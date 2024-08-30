from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUser
from ..models.chatbot import ChatBotModel

@csrf_exempt
def welcome_handler(request):
    but = BitrixUser.objects.filter(is_admin=True).first().bitrix_user_token
    if request.method == 'POST':
        try:
            data = request.POST
            event = data['event']
            if event == 'ONIMBOTJOINCHAT':
                bot_id, dialog_id, bot = get_chat_info(data)
                message = (f'Привет. Я бот по имени {bot["NAME"]} {bot["LAST NAME"]}. Чтобы узнать на что я способен/'
                           f' напиши в чат сообщение с текстом "функционал".')
                response = send_message(but, dialog_id, bot_id, message)

                return JsonResponse({'status': 'ok', 'response': response})

        except Exception as e:

            return JsonResponse({'status': 'error', 'response': str(e)})

    return JsonResponse({'status': 'error', 'response': 'bad request'})

@csrf_exempt
@main_auth(on_cookies=True)
def delete_handler(request):
    but = BitrixUser.objects.filter(is_admin=True).first().bitrix_user_token
    if request.method == 'POST':
        try:
            data = request.POST
            event = data['event']
            if event == 'ONIMBOTDELETE':
                bot_id, dialog_id, bot = get_chat_info(data)
                client_id = data['[data][CLIENT_ID]']
                response = but.call_api_method('imbot.unregister', {'BOT_ID': bot_id, 'CLIENT_ID': client_id})

                return JsonResponse({'status': 'ok', 'response': response})

        except Exception as e:
            response = str(e)

            return JsonResponse({'status': 'error', 'response': response})
    response = 'Некорректный запрос'

    return JsonResponse({'status': 'error', 'response': response})



@csrf_exempt
@main_auth(on_cookies=True)
def message_handler(request):
    but = BitrixUser.objects.filter(is_admin=True).first().bitrix_user_token
    response = 'Некорректный запрос'
    if request.method == 'POST':
        try:
            data = request.POST
            event = data['event']
            if event == 'ONIMBOTMESSAGEADD':
                bot_id, dialog_id, bot = get_chat_info(data)
                user_message = data['data[PARAMS][MESSAGE]']

                if user_message == 'функционал':
                    info_message = ('Чтобы воспользоваться командой, отправь соответвующий текст в следующем сообщении./'
                                    ' Я могу:\n 1. Отправить картинку. Текст "получить картинку"/'
                                    '2. Предоставить ссылку на поисковик. Текст "поисковик"./'
                                    '3. Сообщить данные о погоде в твеом городе. Текст "погода" и через пробел название города на английском языке./')
                    response = send_message(but, dialog_id, bot_id, info_message)


                elif user_message == 'получить картинку':
                    image_link = 'https://upload.wikimedia.org/wikipedia/commons/a/a3/Redhead_Cat_%28%D0%A0%D1%8B%D0%B6%D0%B8%D0%B9_%D0%9A%D0%BE%D1%82%29.jpg'
                    message = 'Держи котика'
                    response = send_message(but, dialog_id, bot_id, message, file=image_link)


                elif user_message == 'поисковик':
                    search_url = 'https://google.com/'
                    response = send_message(but, dialog_id, bot_id, search_url)


                elif 'погода' in user_message:
                    try:
                        city_name = user_message.split(' ')[1]
                        result = requests.get(f'https://api.weatherstack.com/current?access_key=e4cb022f31c56f736d1bfcde5f3210e9&query={city_name}')
                        weather = result.json()['current']

                        cloudcover = ''
                        in_procents = weather['cloudcover']

                        if in_procents <= 10:
                            cloudcover = 'Ясно'
                        elif 10 <= in_procents <= 50:
                            cloudcover = 'Частично облачно'
                        elif 50 <= in_procents <= 100:
                            cloudcover = 'Облачно'

                        message_about_weather = (f'Температура: {weather["temperature"]}\n/'
                                                 f'Скорость ветра: {weather["wind_speed"]}\n/'
                                                 f'Облачность: {cloudcover}/'
                                                 f'Осадки: {weather["precip"]}')

                        response = send_message(but, dialog_id, bot_id, message_about_weather)

                    except Exception as e:
                        response = f'Неверные данные: {str(e)}'

        except Exception as e:
            response = f'Ошибка обработки запроса: {str(e)}'
            return JsonResponse({'status': 'error', 'response': response})

    return JsonResponse({'status': 'error', 'response': response})



def get_chat_info(data):
    bot_id = data['data[PARAMS][BOT_ID]']
    dialog_id = data['data[PARAMS][DIALOG_ID]']
    bot = ChatBotModel.objects.get(bot_id=int(bot_id))
    return bot_id, dialog_id, bot


def send_message(but, dialog_id, bot_id, message, file=''):
    if file:
        response = but.call_api_method('imbot.message.add', {'BOT_ID': bot_id,
                                                             'DIALOG_ID': dialog_id,
                                                             'MESSAGE': message,
                                                             'ATTACH': file})
    else:
        response = but.call_api_method('imbot.message.add', {'BOT_ID': bot_id,
                                                             'DIALOG_ID': dialog_id,
                                                             'MESSAGE': message})
    return response
