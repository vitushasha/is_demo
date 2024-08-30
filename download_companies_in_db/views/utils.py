from download_companies_in_db.models.company_model import CompanyModel
import json

def load_companies(but, first_company_id):
    # Загружаем все ранее не выгруженные компании в БД

    companies = but.call_list_method('crm.company.list', {'order': {'ID': 'ASC'}})

    companies = list(filter(lambda x: int(x['ID']) > first_company_id, companies))

    companies = {elem['ID']: elem for elem in companies}
    for id, data in companies.items():
        data.pop('ID')
        data_json = json.dumps(data)
        CompanyModel.objects.create(id=id, data=data_json)

def db_is_not_empty():
    # Проверяем, есть ли компании в нашей БД, чтобы взять последний id из БД

    objects = CompanyModel.objects.all()
    if objects:
        last_obj = max(objects, key=lambda x: x.id)
        return last_obj.id
    else:
        return 0