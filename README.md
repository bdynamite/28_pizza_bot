# Telegram Bot for Pizzeria

This project consists of a database with an admin view for making changes in db and telegram-bot for users.

# How to Use

Step 1. Register new telegram bot for development purposes, get the new token. [@BotFather](https://telegram.me/botfather)

Step 2. Download project, create virtualenv and install requirements

```
#!bash
# download project, create virtualenv and install requirements
git clone https://github.com/romabiker/28_pizza_bot.git
cd 28_pizza_bot
Scripts/activate
pip install -r requirements.txt
```

Step 3. Create and fill database

```
#!bash
# set vars for app by default or your own
set DB_PATH = sqlite:///pizza.db
set BASIC_AUTH_USERNAME = admin
set BASIC_AUTH_PASSWORD = admin

# environment is ready, just run script
models.py

# now you can manage your db via flask-admin
server.py
```
<http://127.0.0.1:5000/admin>

Step 4. Run the bot
```
#!bash
# set your bot token
set BOT_TOKEN = <your_token>

# run the bot and visit it in telegram
bot.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
