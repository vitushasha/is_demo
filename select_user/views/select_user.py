from django.shortcuts import render
import json
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def select_user(request):
    but = request.bitrix_user_token
    userinfo = None

    if request.method == 'POST':
        user_id = request.POST.get('info')
        userinfo = but.call_api_method('user.get', {'ID': str(user_id)})['result'][0]

    return render(request, 'select_user.html', {'userinfo': userinfo})
