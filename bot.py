import telebot
from jinja2 import Template
from os import getenv
from app import db
from models import Pizza, Choice
import re

TOKEN = getenv('BOT_TOKEN')
if not TOKEN:
    raise Exception('BOT_TOKEN should be specified')

bot = telebot.TeleBot(TOKEN)

with open('templates/catalog.md', 'r', encoding='utf-8') as catalog_file:
    catalog_tmpl = Template(catalog_file.read())

with open('templates/greetings.md', 'r', encoding='utf-8') as greetings_file:
    greetings_tmpl = Template(greetings_file.read())


def get_catalog_list():
    pizzas_list = []
    pizzas = db.session.query(Pizza, Choice).filter(Pizza.active == '1'). \
        join(Choice, Choice.pizza_id == Pizza.pizza_id).all()
    for pizza_id in set([pizza[0] for pizza in pizzas]):
        pizza = {
            'title': pizza_id.title,
            'description': pizza_id.description,
            'choices': [
                {
                    'title': '{} см, {} гр (арт. {})'.format(
                        pizza_coice[1].height,
                        pizza_coice[1].weight,
                        pizza_coice[1].id
                    ),
                    'price': pizza_coice[1].price
                }
                for pizza_coice in list(filter(lambda x: x[0].pizza_id == pizza_id.pizza_id, pizzas))
            ]
        }
        pizzas_list.append(pizza)
    return pizzas_list


@bot.message_handler(commands=['start', 'help'])
def greet(message):
    bot.send_message(message.chat.id, greetings_tmpl.render())


@bot.message_handler(commands=['menu'])
def show_catalog(message):
    bot.send_message(message.chat.id, catalog_tmpl.render(catalog=get_catalog_list()), parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text.startswith('?'))
def calculate_order(message):
    articles = list(map(int, re.findall(r'\d+', message.text)))
    prices = {article: price for article, price in
              db.session.query(Choice.id, Choice.price).filter(Choice.id.in_(articles)).all()}
    msg = 'Ваш заказ составляет {} рублей'.format(sum([prices[article] for article in articles]))
    bot.send_message(message.chat.id, msg)

if __name__ == '__main__':
    bot.polling(none_stop=True)
