import os

import requests
from django.conf import settings
from django.shortcuts import render

from .utils import DataImporter
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param


@main_auth(on_cookies=True)
# достает из GET, POST, json тела парметры
@get_params_from_sources
def load_from_googledocs(request):
    objects_counts = {}
    response = ''

    # Ожидаем что люди нам будут скармливать ссылки типа https://docs.google.com/spreadsheets/d/1ZuKXEK0hwJyxFwGxoi77G0PaOh4Qg4SDZBNkHDws2iU/edit#gid=1891471437
    # а нам нужно вместо edit, делать export
    # сделаем преобразование разбиением строки. Может сбойнуть если id документа будет начинаться с edit
    if request.method == 'POST':
        but = request.bitrix_user_token
        try:
            link = request.POST.get('link')
            export_link = link.split("/edit")[0] + '/export'
            res = requests.get(export_link)
            filename = os.path.join(settings.BASE_DIR, 'temp.xlsx')
            with open(filename, "wb") as f:
                f.write(res.content)
            importer = DataImporter(filename, but)

            objects_counts = importer.import_data_from_xls()
            response = 'Успешно'
        except Exception as e:
            response = 'Произошла ошибка'

    return render(request, 'my_demodata.html', {'objects_counts': objects_counts, 'response': response})
