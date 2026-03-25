import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from Database import Database
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
keep_alive() 

# Инициализация базы данных должна происходить в асинхронной функции
# db = Database('./database.db')  # СТАРЫЙ КОД - удалить
db = Database()  # Новый инстанс, инициализация через await init_db() в main
bot = AsyncTeleBot(token=os.getenv("TOKEN"))


