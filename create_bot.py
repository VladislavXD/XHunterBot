import telebot
import os
from Database import Database
from handlers.keep_alive import keep_alive


keep_alive()




db = Database('./database.db')
bot = telebot.TeleBot(token=os.getenv('TOKEN'))
bot.remove_webhook()
