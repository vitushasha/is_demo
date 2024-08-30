from django.urls import path
from .views.create_chat_bot import create_chat_bot
from .views.handler import welcome_handler, message_handler, delete_handler


app_name = 'chat_bot'


urlpatterns = [
    path('create_chat_bot/', create_chat_bot, name='create_chat_bot'),
    path('welcome_handler/', welcome_handler, name='welcome_handler'),
    path('message_handler/', message_handler, name='message_handler'),
    path('delete_handler/', delete_handler, name='delete_handler'),
]