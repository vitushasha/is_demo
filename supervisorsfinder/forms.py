from django import forms
from integration_utils.bitrix24.models.bitrix_user import BitrixUser


class SelectUserForm(forms.Form):
    but = BitrixUser.objects.filter(is_admin=True).first().bitrix_user_token
    choices = [(user['ID'], user['NAME']) for user in but.call_list_method('user.get')]
    choices.append((None, 'все сотрудники'))
    user = forms.ChoiceField(
        choices=choices, required=False, help_text='Выберите пользователя'
    )

