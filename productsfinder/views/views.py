from django.shortcuts import render
from ..forms import EntityForm
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from collections import Counter


@main_auth(on_cookies=True)
def products_finder(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.cleaned_data['entity']
            res = but.call_list_method(f'crm.{entity}.list')
            lst = list()
            for i in res:
                lst.append(i['NAME'])
            res = {name: count for name, count in Counter(lst).items() if count > 1}
            if len(res) == 0:
                res.setdefault('Дубликатов', 'Нет')
            return render(request, 'productsfinder.html', {'res': res})
    form = EntityForm()
    return render(request, 'productsfinder.html', {'form': form})