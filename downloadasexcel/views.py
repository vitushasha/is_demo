from django.shortcuts import render, redirect
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import os
import settings
import pandas as pd


@main_auth(on_cookies=True)
def get_products(request):
    but = request.bitrix_user_token
    products_dict = but.call_list_method('crm.product.list')
    df = pd.DataFrame(products_dict)
    file_path = os.path.join(settings.MEDIA_ROOT, 'excel_files', 'products.xlsx')
    df.to_excel(file_path, index=False)
    file_url = os.path.join(settings.MEDIA_URL, 'excel_files', 'products.xlsx')

    return render(request, 'downloadasexcel.html', {'file_path': file_url})