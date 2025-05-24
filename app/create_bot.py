import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from Database import Database  # Если `Database` работает синхронно, нужно переделать
# from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
# keep_alive() 

db = Database('./database.db')
bot = AsyncTeleBot(token='6725080038:AAH9HLWT6_ORc9U15jkVo06DIOQMjk17P-c')


# 6725080038:AAH9HLWT6_ORc9U15jkVo06DIOQMjk17P-c