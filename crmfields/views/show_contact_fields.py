from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.shortcuts import render
import json


fields = ['NAME', 'LAST_NAME', 'ID', 'EMAIL']


@main_auth(on_cookies=True)
def show_fields(request):
    res = request.bitrix_user_token.call_list_method('user.get')
    users = []
    for elem in res:
        user = {}
        for field in fields:
            if elem[field]:
                user[field] = elem[field]
            else:
                user[field] = 'Значение не указано'
        users.append(user)
    return render(request, 'showcontactfields.html', {'users': json.dumps(users)})
