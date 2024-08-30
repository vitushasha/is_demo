from download_companies_in_db.views.utils import db_is_not_empty, load_companies
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.http import HttpResponse


@main_auth(on_cookies=True)
def sync_companies(request):
    but = request.bitrix_user_token
    first_company_id = db_is_not_empty()
    try:
        last_company_id = but.call_list_method('crm.company.list', {'order': {'ID': 'DESC'}})[0]['ID']

        if str(first_company_id) != last_company_id:
            load_companies(but, first_company_id)
            return HttpResponse('success')
        else:
            return HttpResponse('Нет новых компаний')

    except Exception as e:
        return HttpResponse(e)



