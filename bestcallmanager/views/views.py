from django.shortcuts import render
from best_call_manager.utils.table_creation import get_html_row, get_html_table
from best_call_manager.utils.api_methods import *
from bestcallmanager.forms.forms import ChoiceUserForm
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import html
from best_call_manager.utils.setting_goals import setting_goals
from best_call_manager.utils.datetime_utils import get_now_date


@main_auth(on_cookies=True)
def create_tasks(request):
    choice_user_form = ChoiceUserForm()
    if request.method == "POST":
        but = request.bitrix_user_token
        now_date = get_now_date()
        choice_user_form = ChoiceUserForm(request.POST)
        if choice_user_form.is_valid():
            user_id = choice_user_form.cleaned_data['user_id']
            try:
                app_date = get_app_date(but)

                if app_date == now_date:
                    return render(request, "best_call_manager.html", {'choice_user_form': choice_user_form})
                else:
                    calls = get_new_calls(but, app_date, now_date, user_id)

            except (TypeError, KeyError):
                calls = get_old_calls(but, now_date, user_id)

            task_id_list, possible_calls = setting_goals(but, calls, user_id)

            app_possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]
            if app_possible_calls and type(app_possible_calls) is dict:
                app_possible_calls.update(possible_calls)
            else:
                app_possible_calls = possible_calls

            app_tasks_id = get_app_tasks_id(but)
            if app_tasks_id and app_tasks_id[0] != '':
                app_tasks_id.extend(task_id_list)
            else:
                app_tasks_id = task_id_list

            set_app_tasks_id(but, app_tasks_id)
            but.call_api_method("app.option.set", {"options": {"possible_calls": app_possible_calls}})
            set_app_date(but, now_date)

    return render(request, "best_call_manager.html", {'choice_user_form': choice_user_form})

@main_auth(on_cookies=True)
def show_best_calls(request):
    """Позволяет собрать все результаты завершенных задач. Создает группу
    если она не существует, а если существует берет ее id. По результату
    задач находит нужный звонок и делает пост с таблицей лучших звонков
    каждого менеджера."""
    choice_user_form = ChoiceUserForm()
    if request.method == "POST":
        but = request.bitrix_user_token
        group = get_app_group(but)
        if group["result"]:
            group_id = group["result"][0]["ID"]
        else:
            group_id = create_app_group(but)

        app_tasks_id = get_app_tasks_id(but)
        if not app_tasks_id or app_tasks_id[0] == '':
            return render(request, 'best_call_manager.html', {'choice_user_form': choice_user_form})

        app_tasks = get_app_tasks(but, app_tasks_id)

        progress_tasks_id = app_tasks_id if app_tasks_id else []
        completed_tasks = dict()

        for app_task in app_tasks:
            if app_task["status"] == '5':
                progress_tasks_id.remove(app_task["id"])
                completed_tasks[app_task["id"]] = app_task

        if not completed_tasks:
            return render(request, 'best_call_manager.html', {'choice_user_form': choice_user_form})

        possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]

        calls = dict()
        for task_id, task in completed_tasks.items():
            try:
                task_res = get_task_res(but, task_id)
            except IndexError:
                progress_tasks_id.append(task_id)

                but.call_api_method("tasks.task.renew", {"taskId": task_id})
                but.call_api_method("task.commentitem.add", {
                    "TASKID": task_id,
                    "FIELDS": {
                        "AUTHOR_ID": task["createdBy"],
                        "POST_MESSAGE": "Оставьте комментарий помеченный как результат"
                    }
                })

                continue

            if type(possible_calls) is dict and possible_calls.get(task_id):
                if not (task_res["text"] in possible_calls[task_id]):
                    progress_tasks_id.append(task_id)

                    but.call_api_method("tasks.task.renew", {"taskId": task_id})
                    but.call_api_method("task.commentitem.add", {
                        "TASKID": task_id,
                        "FIELDS": {
                            "AUTHOR_ID": task["createdBy"],
                            "POST_MESSAGE": "Укажите корректный id звонка"
                        }
                    })

                    continue
                else:
                    del possible_calls[task_id]

            calls[task_res["text"]] = task["responsible"]["name"]

        set_app_tasks_id(but, progress_tasks_id)
        but.call_api_method("app.option.set", {"options": {"possible_calls": possible_calls}})

        app_calls = get_app_calls(but, list(calls.keys()))

        rows = ""
        for counter, app_call in enumerate(app_calls, 1):
            row = get_html_row(app_call, calls, counter)
            rows += row

        html_table = get_html_table(rows)
        add_post(but, f"{html.unescape(html_table)}", [f"SG{group_id}"])

    return render(request, "best_call_manager.html", {'choice_user_form': choice_user_form})