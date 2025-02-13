import telebot
import os
from Database import Database
from keep_alive import keep_alive


keep_alive()




db = Database('./database.db')
bot = telebot.TeleBot(token=os.environ.get('TOKEN'))
bot.remove_webhook()


