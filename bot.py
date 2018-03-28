import telebot
from jinja2 import Template
from os import getenv
from app import db
from models import Pizza
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
    all_available_pizzas = db.session.query(Pizza).filter(Pizza.active == '1')
    pizzas_list = []
    for pizza_type in all_available_pizzas.group_by(Pizza.title).all():
        pizza = {'title': pizza_type.title,
                 'description': pizza_type.description,
                 'choices': [{'title': '{}см, {}гр (арт. {})'.format(pizza_coice.height, pizza_coice.weight,
                                                                     pizza_coice.pizza_id),
                              'price': pizza_coice.price}
                             for pizza_coice in all_available_pizzas.filter(Pizza.title == pizza_type.title).all()]}
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
              db.session.query(Pizza.pizza_id, Pizza.price).filter(Pizza.pizza_id.in_(articles)).all()}
    msg = 'Ваш заказ составляет {} рублей'.format(sum([prices[article] for article in articles]))
    bot.send_message(message.chat.id, msg)

if __name__ == '__main__':
    bot.polling(none_stop=True)
