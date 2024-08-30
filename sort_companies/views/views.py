from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def sort_companies(request):
    flag = False
    if request.method == 'POST':
        but = request.bitrix_user_token
        companies = but.call_list_method('crm.company.list', {'select': ['TITLE']})

        field_id, field = get_user_field(but)
        field = add_list_param(but, companies, field)
        edited_companies_list = create_edited_list(field['LIST'])
        sorted_edited_companies_list = sorted(edited_companies_list, key=lambda x: x['VALUE'])

        sorted_companies_list = []
        companies_dict = {company['ID']: company for company in field['LIST']}
        for sort, company in enumerate(sorted_edited_companies_list):
            companies_dict[company['ID']]['SORT'] = sort + 1
            sorted_companies_list.append(companies_dict[company['ID']])
        result = but.call_api_method('crm.company.userfield.update', {'ID': field_id, 'FIELDS': {'LIST': sorted_companies_list}})
        flag = True

    return render(request, 'sort_companies.html', {'flag': flag})

def add_list_param(but, companies, res):

    if not ('LIST' in res):
        company_list_for_userfield = []
        for index, company in enumerate(companies):
            company_list_for_userfield.append({'VALUE': company['TITLE'], 'SORT': index})
        but.call_api_method('crm.company.userfield.update', {'ID': res['ID'], 'FIELDS': {'LIST': company_list_for_userfield}})
        res = but.call_list_method('crm.company.userfield.list', {'FILTER': {'FIELD_NAME': 'UF_CRM_1724432643'}})[0]
        return res

    else:
        return res

def get_user_field(but):
    userfield = but.call_list_method('crm.company.userfield.list', {'FILTER': {'FIELD_NAME': 'UF_CRM_1724432643'}})[0]
    field_id = userfield['ID']
    return field_id, userfield

def create_edited_list(field_list):
    edited_companies_list = []
    for elem in field_list:
        edited_elem = elem.copy()
        if 'ё' in edited_elem['VALUE']:
            edited_elem['VALUE'] = edited_elem['VALUE'].lower().replace('ё', 'е')
        edited_companies_list.append(edited_elem)

    return edited_companies_list