from django import forms
from ..models.chatbot import ChatBotModel

colors = [
    ("RED", "Красный"),
    ("GREEN", "Зеленый"),
    ("MINT", "Мятный"),
    ("LIGHT_BLUE", "Голубой"),
    ("DARK_BLUE", "Темно-синий"),
    ("PURPLE", "Фиолетовый"),
    ("AQUA", "Аква"),
    ("PINK", "Розовый"),
    ("LIME", "Лайм"),
    ("BROWN", "Коричневый"),
    ("AZURE", "Лазурный"),
    ("KHAKI", "Хаки"),
    ("SAND", "Песочный"),
    ("MARENGO", "Маренго"),
    ("GRAY", "Серый"),
    ("GRAPHITE", "Графит")
]

genders = [('M', 'Мужской'),('F', 'Женский')]

types = [('B', 'ответы поступают сразу'), ('O', 'для открытых линий'), ('S', 'Чат бот с повышенными привилегиями')]


class ChatBotForm(forms.ModelForm):
    PERSONAL_GENDER = forms.ChoiceField(choices=genders, help_text='Пол')
    COLOR = forms.ChoiceField(choices=colors, help_text='Цвет для мобильного приложения')
    TYPE = forms.ChoiceField(choices=types, help_text='Тип бота')

    class Meta:
        model = ChatBotModel
        exclude = ['bot_id', 'EVENT_WELCOME_MESSAGE', 'EVENT_MESSAGE_ADD', 'EVENT_BOT_DELETE']
        widgets = {
            'PERSONAL_BIRTHDAY': forms.DateInput(attrs={'type': 'date'}),
        }