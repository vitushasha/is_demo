from django import forms
from django.forms import DateInput

from call_register.models.models import CustomCallInfo


class CustomCallInfoForm(forms.ModelForm):
    class Meta:
        model = CustomCallInfo
        fields = ['user_phone', 'user_id', 'phone_number', 'call_date',
                  'type', 'add_to_chat', 'file', 'vote']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_phone'].label = 'Внутренний номер пользователя'
        self.fields['user_id'].label = 'Идентификатор пользователя'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['call_date'].label = 'Дата/время звонка'
        self.fields['type'].label = 'Тип звонка'
        self.fields['add_to_chat'].label = 'Уведомление сотрудника Б24'
        self.fields['file'].label = 'Файл с записью звонка (.mp3)'
        self.fields['vote'].label = 'Оценка звонка'
        self.fields['call_date'].widget = DateInput(
            attrs={'type': 'datetime-local'})