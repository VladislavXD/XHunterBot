import telebot
import os
from Database import Database


db = Database('./database.db')
bot = telebot.TeleBot(token=os.environ.get('TOKEN'))
bot.remove_webhook()
