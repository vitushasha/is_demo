from django.shortcuts import render, redirect

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from call_register.forms import CustomCallInfoForm



@main_auth(on_cookies=True)
def reg_call(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        form = CustomCallInfoForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.telephony_externalcall_register(but)
            model.telephony_externalcall_finish(but)
            model.telephony_externalCall_attachRecord(but)
            # model.wav_maker_n_messages(but)
            return redirect('call_register:reg_call')
    form = CustomCallInfoForm()
    return render(request, 'register_call.html', {'form': form})