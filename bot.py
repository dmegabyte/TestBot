import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_KEY
from pymystem3 import Mystem
import requests

bot = telebot.TeleBot(API_KEY)

def get_course_func():
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    value = round(data['Valute']['USD']['Value'], 1)
    return value

def username_func(text):
    m = Mystem()
    analyze = m.analyze(text)
    name = ''
    first_name = ''
    second_name = ''
    middle_name = ''

    for word in analyze:
        try:
            if 'analysis' in word and word['analysis']:
                analysis = word['analysis'][0]
            else:
                continue
        except KeyError:
            continue

        if 'имя' in analysis['gr']:
            first_name = word['text'].capitalize()
        elif 'фам' in analysis['gr']:
            second_name = word['text'].capitalize()
        elif 'отч' in analysis['gr']:
            middle_name = word['text'].capitalize()
        name = f'{first_name} {second_name} {middle_name}'.strip()

    return name

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Добрый день. Как вас зовут?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    name = username_func(message.text)

    if len(name) == 0:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя или используйте команду /start.")
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Перезагрузить бота", callback_data="start"))    
        bot.send_message(message.chat.id, f"Рад знакомству, {name}! Курс доллара сегодня {get_course_func()} рублей за доллар", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "start":
        send_welcome(call.message)

if __name__ == "__main__":
    bot.polling(none_stop=True)