import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from Database import Database  # Если `Database` работает синхронно, нужно переделать

from dotenv import load_dotenv





db = Database('./database.db')
bot = AsyncTeleBot(token=os.getenv('TOKEN'))


