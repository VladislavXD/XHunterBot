import os
from dotenv import load_dotenv
import asyncio
from create_bot import bot

load_dotenv()
_admin_id_raw = os.getenv('ADMIN_ID', '').strip()
ADMIN_ID = int(_admin_id_raw) if _admin_id_raw.isdigit() else 0

import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
import handlers.media_handler
import handlers.osint.searchUser
import handlers.osint.search_by_photo
from Database.DB import init as init_db

async def main():   
    await init_db() # Инициализация базы данных
    await bot.remove_webhook()  # Удаляем вебхук, если он был установлен
    await bot.infinity_polling()
    
    
    
if __name__ == "__main__":
    asyncio.run(main())  # Запуск бота


