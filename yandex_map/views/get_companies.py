from django.http import JsonResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def get_companies(request):
    but = request.bitrix_user_token
    companies = but.call_list_method('crm.company.list')
    companies = {company['ID']: company['TITLE'] for company in companies}
    addresses = but.call_list_method('crm.address.list', {
        'order': {'TYPE_ID': 'ASC'},
        'select': ['ADDRESS_1', 'CITY', 'PROVINCE', 'COUNTRY', 'ANCHOR_ID'],
        'filter': {'ANCHOR_TYPE_ID': '4'}
    })
    comp_with_addr = {}
    for addr in addresses:
        comp_id = addr['ANCHOR_ID']
        if addr['ANCHOR_ID'] in companies:
            comp_with_addr.setdefault(comp_id, {})
            comp_with_addr[comp_id].setdefault('addr', [])
            comp_with_addr[comp_id]['addr'].append(addr)
            comp_with_addr[comp_id]['title'] = companies[comp_id]

    return JsonResponse(comp_with_addr)