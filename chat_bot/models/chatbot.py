from django.db import models
import base64
import settings


class ChatBotModel(models.Model):
    # Модель, описывающая чат-бота, его тип и персональные данные

    # Настроечные параметры бота
    bot_id = models.IntegerField(primary_key=True)
    TYPE = models.CharField(max_length=1) # Тип бота
    CODE = models.CharField(max_length=255, help_text='Строковый идентификатор бота')

    # Обработчики событий, ответ на сообщения боту, его функционал
    EVENT_MESSAGE_ADD = models.URLField(max_length=500, help_text='Обработчик входящих сообщений')
    EVENT_WELCOME_MESSAGE = models.URLField(max_length=500, help_text='Обработчик приветствия, начало работы')
    EVENT_BOT_DELETE = models.URLField(max_length=500, help_text='Обработчик запроса об удалении чат бота')

    # Персональные данные чат-бота
    NAME = models.CharField(max_length=255, help_text='Имя бота')
    LAST_NAME = models.CharField(max_length=255, help_text='Фамилия Бота')
    EMAIL = models.EmailField(max_length=255, help_text='Введите email, не совпадает с адресами настоящих пользователей')
    COLOR = models.CharField(max_length=50) # Цвет для мобильного приложения
    PERSONAL_BIRTHDAY = models.DateField(help_text='День рождения')
    WORK_POSITION = models.TextField(help_text='Описание чат-бота')
    PERSONAL_WWW = models.URLField(max_length=500, help_text='Ссылка на сайт')
    PERSONAL_GENDER = models.CharField(max_length=1) # Пол бота
    PERSONAL_PHOTO = models.ImageField(upload_to='bot_photo/', default='default.jpg', blank=True)


    def get_properties(self):
        # Возвращаем словарь с персональными данными бота для метода imbot.register
        file_path = settings.MEDIA_ROOT.replace('\\', '/') + '/' + self.PERSONAL_PHOTO.name

        properties = {
            "NAME": self.NAME,
            "LAST_NAME": self.LAST_NAME,
            "EMAIL": self.EMAIL,
            "COLOR": self.COLOR,
            # Преобразуем дату в строку формата 'YYYY-MM-DD'
            "PERSONAL_BIRTHDAY": self.PERSONAL_BIRTHDAY.strftime('%Y-%m-%d'),
            "WORK_POSITION": self.WORK_POSITION,
            "PERSONAL_WWW": self.PERSONAL_WWW,
            "PERSONAL_GENDER": self.PERSONAL_GENDER,
        }

        with open(file_path, 'rb') as photo:
            properties["PERSONAL_PHOTO"] = base64.b64encode(photo.read())

        return properties