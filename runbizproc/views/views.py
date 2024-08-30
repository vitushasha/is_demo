from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..models.models import BizProcModel
from ..forms import BPForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@main_auth(on_cookies=True)
def run_bizproc(request):
    but = request.bitrix_user_token
    companies_id = but.call_list_method('crm.company.list', {'select': ['ID']})
    BizProcModel.find_all_bizprocs(but)
    if request.method == 'POST':
        form = BPForm(request.POST)
        if form.is_valid():
            cur_bp = form.cleaned_data['bp']
            but.call_api_method('log.blogpost.add',
                                {'USER_ID': str(but.user.bitrix_id),
                                 'POST_MESSAGE': 'Бизнес процесс запущен',
                                 'POST_TITLE': 'Уведомление',
                                 'DEST': 'UA'})
            for company in companies_id:
                cur_bp.run_cur_bizproc(but, company['ID'])

            return HttpResponseRedirect(reverse('reload_start'))

    form = BPForm()
    return render(request, 'runbizproc.html', {'form': form})