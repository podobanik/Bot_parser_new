import time

import requests
from bs4 import BeautifulSoup as b
import telebot

TOKEN="6113685540:AAFL-yuCDtErkyI0j8dAwGbMDNtS9GoRt2U"
URL = 'https://knastu.ru/'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    news = soup.find_all('div', class_='post-text-excerpt')
    return [i.text for i in news]


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def print_queue(self):
        print(self.items)


list_of_news = parser(URL)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте, чтобы узнать последние новости университета, введите цифру от 1 до 5:')


@bot.message_handler(content_types=['text'])
def news(message):
    q = Queue()
    q.enqueue(message.text.lower())
    while not q.is_empty():
        out = q.dequeue()
        if out in ['1', '2', '3', '4', '5']:
            bot.send_message(message.chat.id,list_of_news[int(out)-1]+'{}'.format(URL))
            #del list_of_news[0]
        else:
            bot.send_message(message.chat.id,'Наш бот предоставляет только самые свежие новости! (Введите цифру от 1 до 5):')


bot.polling()