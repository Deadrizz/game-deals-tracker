import telebot
import requests
import os

from dotenv import load_dotenv

load_dotenv()
TBOT_API_TOKEN = os.getenv('TBOT_API_TOKEN')
bot = telebot.TeleBot(TBOT_API_TOKEN)
API_URL = os.getenv('API_URL')
pending_add = {}
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id,f'Hello! This bot will be send notifications about new game deals.There is your chat id:{user_id}')

@bot.message_handler(commands=['subs'])
def sub(message):
    user_id = message.chat.id
    request = requests.get(f'{API_URL}/api/subscriptions/?chat_id={user_id}')
    data = request.json()
    if data['count'] == 0:
        bot.send_message(user_id,'You have 0 subscriptions.You should change it!')
        return None
    for sub in data['results']:
        id = sub['id']
        min_discount = sub['min_discount']
        max_price = sub['max_price']
        query = sub['query']
        if sub['store_name'] is not None:
            store_name = sub['store_name']
            bot.send_message(user_id,f'You have subscription for {query} in {store_name} with minimal discount: {min_discount} and maximum price: {max_price} by ID: {id}')
        else:
            bot.send_message(user_id,f'You have subscription for {query} in Any Store with minimal discount:{min_discount} and maximum price:{max_price} by ID:{id}')
    return None

@bot.message_handler(commands=['check'])
def check(message):
    user_id = message.chat.id
    request = requests.post(f'{API_URL}/api/notification/generate/?chat_id={user_id}')
    if request.status_code !=200:
        bot.send_message(user_id,'We have some problem with our data.Please try again later<3')
        return 0
    data = request.json()
    created = data['created']
    bot.send_message(user_id,f'New notifications created:{created}')



@bot.message_handler(commands=['add'])
def add(message):
    user_id = message.chat.id
    pending_add[user_id] = True
    bot.send_message(message.chat.id,'Please send me data about what you wanna start to follow.For exemple:minimum discount,maximum price,query,(if you want u can add store)')


@bot.message_handler(func=lambda m: pending_add.get(m.chat.id) is True and m.text and not m.text.startswith("/"))
def text_message(message):
    user_id = message.chat.id
    if pending_add.get(user_id) != True:
        return None
    else:
        data = message.text.split(' ')
        min_discount = int(data[0])
        max_price = data[1]
        query = data[2:]
        query_text = " ".join(query)
        json = {'min_discount':min_discount,'max_price':max_price,'query':query_text}
        request = requests.post(f'{API_URL}/api/subscriptions/?chat_id={user_id}',json=json)
        if request.status_code == 201:
            data = request.json()
            id = data['id']
            bot.send_message(user_id,f'Created subscription #{id}')
            pending_add[user_id] = False
        else:
            bot.send_message(user_id,'Error')
            pending_add[user_id] = True
            return None


@bot.message_handler(commands=['notify'])
def notify(message):
    user_id = message.chat.id
    bot.send_message(user_id,'Calling api')
    request = requests.post(f'{API_URL}/api/notification/dispatch/?chat_id={user_id}',timeout=5)
    if request.status_code == 200:
        data = request.json()
        if data['count'] == 0:
            bot.send_message(user_id,'No new deals')
            return None
        for item in data['items']:
            title = item['title']
            store = item['store']
            sale_price = item['sale_price']
            discount = item['discount_percent']
            url = item['url']
            if store is not None:
                bot.send_message(user_id,f'You have deals(Title:{title},store:{store},sale price:{sale_price},discount:{discount},url:{url})')
            else:
                bot.send_message(user_id,f'You have deals(Title:{title},store:Any store,sale price:{sale_price},discount:{discount},url:{url})')
        return None
bot.polling()