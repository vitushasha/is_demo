from django import forms

class EntityForm(forms.Form):
    entities = [
        ('lead', 'Лиды'),
        ('company', 'Компании'),
        ('contact', 'Контакты'),
        ('deal', 'Сделки'),
    ]
    entity = forms.ChoiceField(choices=entities, required=True, help_text='Выберите сущность')