import telebot
import os
from Database import Database
from keep_alive import keep_alive


# keep_alive()




db = Database('./database.db')
bot = telebot.TeleBot(token='7654585303:AAFLJMpcU2znRSbob-KPUgM0XZE1QTqDR3k')
bot.remove_webhook()
