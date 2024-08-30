from django.http import HttpResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.large_utils import keep_call_info_synced

import threading


@main_auth(on_cookies=True)
def keep_synced(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        bot_token = request.POST.get('bot_token')
        calls_chat_id = request.POST.get('calls_chat_id')
        sync_loop = threading.Thread(target=keep_call_info_synced, args=(but, bot_token, calls_chat_id), daemon=True)
        sync_loop.start()
        return HttpResponse("Continuous synchronization is ongoing")
    return render(request, 'send_button_page.html')