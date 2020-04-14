import random
import requests
import vk_api
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3

conn = sqlite3.connect("db.db")
c = conn.cursor()
api_url = "http://api.openweathermap.org/data/2.5/weather"
vk_session = vk_api.VkApi(token='bce07b529888ef3bfb494dd8f07e5587c582a47db3dd0c5e564d9c4283a10b41c2a56b7e23f5ca326f041')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def create_keyboard ():
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Узнать погоду', color='primary')
    keyboard.add_button('Что мне надеть?', color='primary')

    keyboard = keyboard.get_keyboard()
    return keyboard

def create_keyboard2():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Для этого города', color='primary')
    keyboard.add_button('Для другого города', color='primary')

    keyboard = keyboard.get_keyboard()
    return keyboard

def create_keyboard3():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Ввести заново', color='primary')

    keyboard = keyboard.get_keyboard()
    return keyboard

def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

def create_new_user(user_id):
    cmd = "INSERT INTO users(id, country, region, city) VALUES('%s', '%s', '%s', '%s')" % (user_id, '1', '?', '?')
    c.execute(cmd)
    conn.commit()

def check_to_fill(user_id):
    c_country = "SELECT country FROM users WHERE id = '%s'" % user_id
    c_region = "SELECT region FROM users WHERE id = '%s'" % user_id
    c_city = "SELECT city FROM users WHERE id = '%s'" % user_id
    c.execute(c_country)
    result = c.fetchone()
    if result[0] == "1":
        return "country"
    else:
        c.execute(c_region)
        result = c.fetchone()
        if result[0] == "1":
            return "region"
        else:
            c.execute(c_city)
            result = c.fetchone()
            if result[0] == "1":
                return "city"
            else:
                return "filled"

def fill_country(user_id, country):
    cmd = "UPDATE users SET country='%s' WHERE id='%s'" % (country, user_id)
    c.execute(cmd)
    cmd = "UPDATE users SET region='%s' WHERE id='%s'" % ('1', user_id)
    c.execute(cmd)
    conn.commit()

def fill_region(user_id, region):
    cmd = "UPDATE users SET region='%s' WHERE id='%s'" % (region, user_id)
    c.execute(cmd)
    cmd = "UPDATE users SET city='%s' WHERE id='%s'" % ('1', user_id)
    c.execute(cmd)
    conn.commit()

def fill_city(user_id, city):
    cmd = "UPDATE users SET city='%s' WHERE id='%s'" % (city, user_id)
    c.execute(cmd)
    conn.commit()

def get_location(user_id):
    c_country = "SELECT country FROM users WHERE id = '%s'" % user_id
    c_region = "SELECT region FROM users WHERE id = '%s'" % user_id
    c_city = "SELECT city FROM users WHERE id = '%s'" % user_id
    c.execute(c_country)
    country = c.fetchone()
    c.execute(c_region)
    region = c.fetchone()
    c.execute(c_city)
    city = c.fetchone()
    if str(country[0]) == "usa" or str(country[0]) == "us" or str(country[0]) == "united states of america" or str(country[0]) == "united states" or str(country[0]) == 'сша' or str(country[0]) == "соединенные штаты америки":
        location = str(city[0]) + ',' + str(region[0]) + ',' + str(country[0])
    else:
        location = str(city[0]) + ',' + str(country[0])
    return location

def show_weather(user_id):
    keyboard = create_keyboard()
    keyboard3 = create_keyboard3()
    params = {
        'q': get_location(user_id),
        'appid': 'e973fd275eb9fc503e12ff73ea7d5c2a',
        'units': 'metric',
        'lang': 'ru'
    }
    res = requests.get(api_url, params=params)
    if res.status_code == 200:
        data = res.json()
        temp = str(data["main"]["temp"])
        pressure = str(data["main"]["pressure"])
        wind = str(data["wind"]["speed"])
        printout = "Температура - " + temp + " градусов по Цельсию, давление - " + pressure + " гПа, скорость ветра - " + wind + " м/с"
        send_message(vk_session, 'user_id', event.user_id, message=printout, keyboard=keyboard)
    else:
        send_message(vk_session, 'user_id', event.user_id, message="Такой город не найден. Попробуй ввести название города и страны на оригинальном языке или проверь правильность ввода", keyboard=keyboard3)

def what_wear(user_id):
    keyboard3 = create_keyboard3()
    params = {
        'q': get_location(user_id),
        'appid': 'e973fd275eb9fc503e12ff73ea7d5c2a',
        'units': 'metric',
        'lang': 'ru'
    }
    res = requests.get(api_url, params=params)
    if res.status_code == 200:
        data = res.json()
        temp = int(data["main"]["feels_like"])
        if temp >= 15:
            send_message(vk_session, 'user_id', event.user_id,
                         message='Сегодня можно одеться полегче! Надевай свою любимую футболку и кроссы, не замерзнешь:)')
        elif temp >= 5:
            send_message(vk_session, 'user_id', event.user_id,
                         message='Чуть-чуть прохладно, обязательно возьми с собой куртку и надевай закрытую одежду.')
        elif temp >= -5:
            send_message(vk_session, 'user_id', event.user_id,
                         message='Ух, сегодня не жарко! Надевай куртку и обувь потеплее.')
        elif temp >= -15:
            send_message(vk_session, 'user_id', event.user_id,
                         message='Надевай зимнюю одежду, пуховик потеплее, свитер и бабулины шерстянные носки.')
        else:
            send_message(vk_session, 'user_id', event.user_id,
                         message='Настоящая Антарктида! Надевай свой свитер из шерсти единорога, несколько пар носков, зимнюю куртку, сапоги и не забудь шапку, шарф и перчатки!')

        if "дождь" in str(data["weather"][0]["description"].lower()):
            send_message(vk_session, 'user_id', event.user_id, message='Возьми зонтик! Сегодня возможен дождь.')
    else:
        send_message(vk_session, 'user_id', event.user_id, message="Такой город не найден. Попробуй ввести название города и страны на оригинальном языке или проверь правильность ввода", keyboard=keyboard3)

def delete(value):
    cmd = "DELETE FROM users WHERE id=%d" % value
    c.execute(cmd)
    conn.commit()

def check_exist(user_id):
    cmd = "SELECT * FROM users WHERE id = %d" % user_id
    c.execute(cmd)
    result = c.fetchone()
    if result is None:
        return False
    return True

for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            response = event.text.lower()
            keyboard = create_keyboard()
            keyboard2 = create_keyboard2()
            if response == "узнать погоду":
                if check_exist(event.user_id):
                    send_message(vk_session, 'user_id', event.user_id, message='Показать погоду для ' + get_location(event.user_id).replace(',', ', ').title()+'?', keyboard=keyboard2)
                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Напиши мне начать, чтобы начать работу со мной.')
            elif response == "начать":
                if check_exist(event.user_id):
                    delete(event.user_id)
                create_new_user(event.user_id)
                send_message(vk_session, 'user_id', event.user_id, message='Привет! Я подскажу тебе погоду и что надеть, чтобы не замерзнуть сегодня! В какой стране ты живешь?')
            elif response == "для этого города":
                if check_exist(event.user_id):
                    show_weather(event.user_id)
                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Напиши мне начать, чтобы начать работу со мной.')
            elif response == "для другого города" or response == "ввести заново":
                if check_exist(event.user_id):
                    delete(event.user_id)
                create_new_user(event.user_id)
                send_message(vk_session, 'user_id', event.user_id, message='В какой стране ты живешь?')
            elif response == "что мне надеть?":
                if check_exist(event.user_id):
                    what_wear(event.user_id)
                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Напиши мне начать, чтобы начать работу со мной.')
            else:
                if check_exist(event.user_id):
                    if check_to_fill(event.user_id) == "country":
                        fill_country(event.user_id, event.text.lower())
                        send_message(vk_session, 'user_id', event.user_id, message='Какой регион?')
                    elif check_to_fill(event.user_id) == "region":
                        fill_region(event.user_id, event.text.lower())
                        send_message(vk_session, 'user_id', event.user_id, message='Какой город?')
                    elif check_to_fill(event.user_id) == "city":
                        fill_city(event.user_id, event.text.lower())
                        show_weather(event.user_id)
                    else:
                        send_message(vk_session, 'user_id', event.user_id, message='Извини, не разобрал твоего ответа, попробуй снова.')
                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Напиши мне начать, чтобы начать работу со мной.')
    except:
        send_message(vk_session, 'user_id', event.user_id, message='Произошла ошибка! Попробуй снова')