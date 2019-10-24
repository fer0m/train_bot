import telebot
from telebot import types
import requests
import json
import time
import datetime


# Глобальные переменные времени
time_now = str(datetime.datetime.now())[11:16]
date_now = str(datetime.datetime.now())[0:10]

# Информация по боту
bot = telebot.TeleBot('949040094:AAFo6nbxJsUfXLaHxFgwRQ8gfZSqSIIYd8k')

# Код для парса электричек

API = 'ef07933a-471d-462a-a481-3852e0784860'

def info_train(station_1, station_2):
    response = requests.get('https://api.rasp.yandex.net/v3.0/search/?'
                            'apikey=ef07933a-471d-462a-a481-3852e0784860&'
                            'format=json&'
                            'from={station_1}&'
                            'to={station_2}&'
                            'lang=ru_RU&'
                            'transport_types=suburban&'
                            'page=1&'
                            'date={date_now}&'
                            'offset=1&'
                            'limit=10000'.format(station_1=station_1, station_2=station_2, date_now=date_now))

    response.encoding = 'utf-8'
    global page_1
    page_1= json.loads(response.text)
    return page_1

# Колдовство для расчета разницы во времени

def different_time(time:str):
    time_now = str(datetime.datetime.now())[11:16]
    requared_now = time_now.split(':')
    time_now_all = int(requared_now[0])*60 + int(requared_now[1])

    time_train = time
    requared_train = time_train.split(':')
    time_train_all = int(requared_train[0])*60 + int(requared_train[1])

    how_time = str((time_train_all - time_now_all)//60).zfill(2), ":", str((time_train_all - time_now_all) % 60).zfill(2)
    final_time = "".join(how_time)
    return final_time


# Код для работы парсера

def station_parse(station_1, station_2):
    info_train(station_1, station_2)
    list = []
    for i in range(page_1['pagination']['total'] - 1):
        if page_1['segments'][i]['departure'][11:16] > time_now:
            list.append(((' ' + page_1["segments"][i]['thread']['title'] + ". Отправлением в : " +
                          (page_1['segments'][i]['departure'][11:16]) +
                          ". Прибытием в : "
                          + page_1['segments'][i]['arrival'][11:16] +
                          " Отправится через: "
                          + different_time(page_1['segments'][i]['departure'][11:16]))))
        else:
            pass

    go_train = '\n \n'.join(list[0:5])
    return go_train


@bot.message_handler(content_types=['text'])
def start_find(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    keyboard.row(
        telebot.types.InlineKeyboardButton('Едем в Пушкино', callback_data='Пушкино'),
        telebot.types.InlineKeyboardButton('Едем в Москву', callback_data="Москва")
                )

    bot.send_message(message.chat.id, 'Выбери, куда поедешь', reply_markup=keyboard)

# Код для работы бота
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Поехали" or "Го":
        start_find(message)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(message):
    data = message.data
    if data.startswith('Пушкино'):
        station_1 = "s2000002"
        station_2 = "c10748"
        bot.send_message(message.from_user.id, station_parse(station_1, station_2))
    else:
        station_1 = "c10748"
        station_2 = "s2000002"
        bot.send_message(message.from_user.id, station_parse(station_1, station_2))

try:
    bot.polling(none_stop=True, interval=0)
except Exception:
    pass

"""https://www.mindk.com/blog/how-to-develop-a-chat-bot/"""
