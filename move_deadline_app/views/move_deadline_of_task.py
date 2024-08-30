from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.models import BitrixUser
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from datetime import datetime, timedelta


@main_auth(on_cookies=True)
def page_with_button(request):
    button_type = request.GET.get('type')

    if button_type not in ['js', 'admin', 'self']:
        return HttpResponseBadRequest

    script_name = button_type
    if button_type == "self":
        script_name = "admin"

    path_to_script = f"move_tasks_deadline_js/{script_name}.js"

    return render(request, 'page_with_button.html', {'button_type': button_type, "path_to_script": path_to_script})


@main_auth(on_cookies=True)
def move_function(request):
    if request.method != "POST":
        return HttpResponseBadRequest

    task_id = request.POST.get('task_id')
    button_type = request.GET.get('type')

    if button_type in ['admin', 'self']:
        but = BitrixUser.objects.filter(is_admin=True).bitrix_user_token
        deadline_iso = but.call_api_method('tasks.task.get', {'taskid': task_id, 'select': ['DEADLINE']})
        deadline = datetime.fromisoformat(deadline_iso) + timedelta(days=1)
        deadline = deadline.isoformat()
        but.call_api_method('tasks.task.update', {'taskid': task_id, 'fields': {'DEADLINE': deadline}})
    else:
        return HttpResponse('Не правильный тип обработчика')

    return HttpResponse('OK')