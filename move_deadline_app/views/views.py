from django.shortcuts import render, redirect
import settings
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.urls import reverse
from django.http import HttpResponse


@main_auth(on_cookies=True)
def face_page(request):
    # Отображает шаблон

    handler_types = ['js', 'admin', 'self']
    return render(request, 'face_page.html', {'handler_types': handler_types})


@main_auth(on_cookies=True)
def unbind_handler(request):
    handler_types = ['js', 'admin', 'self']
    if request.method == 'POST':
        if request.bitrix_user.is_admin:
            but = request.bitrix_user_token
            type_of_handler = request.POST.get('type')
            if type_of_handler in handler_types:
                answer = has_app_handler(but, type_of_handler)
                if answer != 'Есть хендлер':
                    return HttpResponse('Такого обработчика нет')
                else:
                    handler = 'https://' + settings.DOMAIN + reverse('move_deadline_app:page_with_button') + '?type=' + type_of_handler
                    but.call_api_method('placement.unbind', params={'PLACEMENT': 'TASK_VIEW_SIDEBAR', 'HANDLER': handler})
                    return redirect('move_deadline_app:face_page')
            else:
                HttpResponse('Некорректный тип обработчика')
        else:
            HttpResponse('Только администратор может удалять обработчики')


@main_auth(on_cookies=True)
def bind_handler(request):
    if request.method == 'POST':
        if request.bitrix_user.is_admin:
            but = request.bitrix_user_token
            type_of_handler = request.POST.get('type')
            if type_of_handler in ['js', 'admin', 'self']:
                answer = has_app_handler(but, type_of_handler)
                if answer == 'Есть хендлер':
                    return HttpResponse('Такой обработчик уже есть')
                else:
                    if type_of_handler != 'self':
                        but.call_api_method('placement.bind', params={'PLACEMENT': 'TASK_VIEW_SIDEBAR', 'HANDLER': answer,
                                                               'LANG_ALL': {'ru': {
                                                                   'TITLE': 'Горит срок?',
                                                                   'DESCRIPTIONS': 'Можно его перенести!',
                                                               }}})
                    else:
                        but.call_api_method('placement.bind', params={'PLACEMENT': 'TASK_VIEW_SIDEBAR', 'HANDLER': answer, 'USER_ID': but.user.bitrix_id,
                                                               'LANG_ALL': {'ru': {
                                                                   'TITLE': 'Горит срок?',
                                                                   'DESCRIPTIONS': 'Можно его перенести!',
                                                               }}})
                    return redirect('move_deadline_app:face_page')
            else:
                return HttpResponse('Некорректный тип обработчика')
        else:
            return HttpResponse('Только администратор может добавлять обработчики')


def has_app_handler(but, type):
    response = but.call_api_method('placement.get')['result']

    handler = 'https://' + settings.DOMAIN + reverse('move_deadline_app:page_with_button') + '?type=' + type
    if response:
        has_app_handler = list(filter(lambda x: x['placement'] == 'TASK_VIEW_SIDEBAR' and x['handler'] == handler, response))

        if has_app_handler:
            return 'Есть хендлер'
        else:
            return handler
    else:
        return handler