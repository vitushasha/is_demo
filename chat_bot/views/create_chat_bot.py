from django.shortcuts import render
from django.urls import reverse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms.chat_bot_form import ChatBotForm
import settings


@main_auth(on_cookies=True)
def create_chat_bot(request):
    response = 'Создайте своего чат-бота Битрикс24'
    if request.method == 'POST':
        try:
            if request.bitrix_user.is_admin == True:
                but = request.bitrix_user_token
                form = ChatBotForm(request.POST, request.FILES)
                if form.is_valid():
                    bot = form.save(commit=False)
                    properties = bot.get_properties()
                    bot.EVENT_MESSAGE_ADD = "https://" + settings.DOMAIN + reverse('chat_bot:message_handler')
                    bot.EVENT_WELCOME_MESSAGE = "https://" + settings.DOMAIN + reverse('chat_bot:welcome_handler')
                    bot.EVENT_BOT_DELETE = "https://" + settings.DOMAIN + reverse('chat_bot:delete_handler')
                    bot_id = but.call_api_method('imbot.register', {'CODE': bot.CODE,
                                                                    'EVENT_MESSAGE_ADD': bot.EVENT_MESSAGE_ADD,
                                                                    'EVENT_WELCOME_MESSAGE': bot.EVENT_WELCOME_MESSAGE,
                                                                    'EVENT_BOT_DELETE': bot.EVENT_BOT_DELETE,
                                                                    'TYPE': bot.TYPE,
                                                                    'PROPERTIES': properties,})
                    bot.bot_id = int(bot_id['result'])
                    result = but.call_api_method('imbot.chat.add', {'TYPE': 'CHAT',
                                                                    'TITLE': 'Чат с тестовым чат-ботом',
                                                                    'COLOR': bot.COLOR,
                                                                    'MESSAGE':'Добро пожаловать',
                                                                    'BOT_ID': bot.bot_id,
                                                                    'USERS': ['1'],
                                                                    'ENTITY_TYPE': 'CHAT'})
                    bot.save()
                    response = 'Бот успешно создан и создан чат - ' + str(result)
            else:
                response = 'Чат-бота может создать только администратор'

        except Exception as e:
            response = str(e)

    form = ChatBotForm()
    return render(request, 'createchatbot.html', {'form': form, 'response': response})