from django import forms
from integration_utils.bitrix24.models import BitrixUser

but = BitrixUser.objects.first().bitrix_user_token
choices = [(user['ID'], user['NAME']) for user in but.call_list_method('user.get')]
choices.append((None, 'Все менеджеры'))
class ChoiceUserForm(forms.Form):
    user_id = forms.ChoiceField(choices=choices, help_text='Выберите менеджера')