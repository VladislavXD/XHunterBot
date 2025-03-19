import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from Database import Database  # Если `Database` работает синхронно, нужно переделать
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

keep_alive() 

db = Database('./database.db')
bot = AsyncTeleBot(token=os.getenv('TOKEN'))


