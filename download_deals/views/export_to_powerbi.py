from django.http import HttpResponseForbidden, JsonResponse
from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.bitrix24.models import BitrixUser

@get_params_from_sources
def download_deals(request):
    if request.its_params.get('s') != "KJBHILiswbeg8yuesbg":
        return HttpResponseForbidden()
    but = BitrixUser.objects.filter(is_admin=True).first().bitrix_user_token
    deals = but.call_list_method('crm.deal.list', {'select': ['ASSIGNED_BY_ID', 'COMPANY_ID', 'CONTACT_ID', 'DATE_CREATE', 'TITLE']})
    for deal in deals:
        contacts_of_deal = but.call_list_method('crm.deal.contact.items.get', {'id': deal['ID']})
        if contacts_of_deal != []:
            deals['CONTACT_ID'] = contacts_of_deal
    companies = but.call_list_method('crm.company.list', {'select': ['ADDRESS', 'ADDRESS_CITY', 'ID', 'LEAD_ID', 'TITLE']})
    contacts = but.call_list_method('crm.contact.list', {'select': ['ID', 'LEAD_ID', 'NAME', 'LAST_NAME', 'COMPANY_IDS']})
    result = {
        'deals': deals,
        'companies': companies,
        'contacts': contacts
    }
    return JsonResponse(result, safe=False)

