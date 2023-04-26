import requests
from bs4 import BeautifulSoup as b
import telebot
from auth_info import TOKEN


URL = 'https://knastu.ru/'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    news_ = soup.find_all('div', class_='post-text-excerpt')
    return [i.text for i in news_]


def parser2(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    all_news_ = soup.find_all('div', class_='block-wrap')
    return [i.text for i in all_news_]


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
list_of_all_news = parser2(URL)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте, чтобы узнать последние новости университета, введите цифру от 1 '
                                      'до 5:')


@bot.message_handler(commands=['news'])
def all_news(message):
    x = 0
    for i in list_of_all_news:
        if x < 5:
            bot.send_message(message.chat.id, i)
            x += 1
    bot.send_message(message.chat.id, 'Информация взята с сайта: {}'.format(URL))


@bot.message_handler(content_types=['text'])
def news(message):
    q = Queue()
    q.enqueue(message.text.lower())
    while not q.is_empty():
        out = q.dequeue()
        if out in ['1', '2', '3', '4', '5']:
            bot.send_message(message.chat.id,list_of_news[int(out)-1]+'{}'.format(URL))
        else:
            bot.send_message(message.chat.id,'Наш бот предоставляет только самые свежие новости! (Введите цифру от 1 '
                                             'до 5):')




if __name__ == '__main__':
    bot.polling()