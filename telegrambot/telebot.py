from sqlparse.utils import offset

from integration_utils.vendors.telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup
from integration_utils.vendors.telegram.utils.request import Request
import requests

request = Request(con_pool_size=8, connect_timeout=500, read_timeout=500)

bot = Bot(token='7306027106:AAFkZGObMMwmPEiuDIbkUkrN39b86A9a-48')

def restart_bot(update):
    keyboard = [
        [KeyboardButton("Перезапуск бота")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="перезапустить бота?", reply_markup=reply_markup)

def get_something(update: Update):
    keyboard = [
        [KeyboardButton("Отправить Картинку"), KeyboardButton("Отправить Стих")],
        [KeyboardButton('Остановить бота')],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text(text="Привет. Этим ботом можно отправить стих или картинку.\nВыберите действие:", reply_markup=reply_markup)

def handle_commands(update: Update):
    chat_id = update.message.chat.id
    user_message = update.message.text

    # Определяем действие
    if user_message == 'Отправить Картинку':
        bot.send_photo(chat_id=chat_id, photo=file_path)
        bot.send_message(chat_id=chat_id, text='Далее')
        get_something(update)
        return None
    elif user_message == "Отправить Стих":
        bot.send_message(chat_id=chat_id, text="Умом Россию не понять,\nАршином общим не измерить:\nУ ней особенная стать —\nВ Россию можно только верить.")
        bot.send_message(chat_id=chat_id, text='Далее')
        get_something(update)
        return None
    elif user_message == 'Перезапуск бота':
        bot.send_message(chat_id=chat_id, text='Перезапуск бота')
        return None
    elif user_message == 'Остановить бота':
        return True

def main():
    global file_path
    file_path = 'https://upload.wikimedia.org/wikipedia/commons/a/a3/Redhead_Cat_%28%D0%A0%D1%8B%D0%B6%D0%B8%D0%B9_%D0%9A%D0%BE%D1%82%29.jpg'
    last_update_id = None

    while True:
        answers = requests.get('https://api.telegram.org/bot7306027106:AAFkZGObMMwmPEiuDIbkUkrN39b86A9a-48/getUpdates').json()['result']
        if answers:
            answer = answers[len(answers)-1]
            chat_id = answer['message']['chat']['id']
            if answer['message']['text'] in ['/start', 'Всего хорошего', 'Перезапуск бота', 'Далее']:
                last_update_id = answer['update_id']
                while True:
                    updates = bot.get_updates(offset=last_update_id)
                    update = updates[len(updates)-1]
                    flag = get_something(update)
                    handle_commands(update)
                    last_update_id = update.update_id + 1
                    if flag:
                        bot.send_message(chat_id, text='Всего хорошего')
                        break
            else:
                bot.send_message(chat_id=chat_id, text='Такой команды нет')
                while True:
                    last_update_id = answer['update_id'] + 1
                    updates = bot.get_updates(offset=last_update_id)
                    if updates:
                        restart_bot(updates[len(updates) - 1])
                        handle_commands(updates[len(updates) - 1])
                        last_update_id += 1
                    else:
                        break



main()