import asyncio
from create_bot import bot
import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
import handlers.media_handler
import handlers.osint.searchUser
import handlers.osint.search_by_photo
import os
from dotenv import load_dotenv  
from Database.DB import init as init_db
load_dotenv()


ADMIN_ID = int(os.getenv('ADMIN_ID'))

async def main():   
    await init_db() # Инициализация базы данных
    await bot.remove_webhook()  # Удаляем вебхук, если он был установлен
    await bot.infinity_polling()
    
    
    
if __name__ == "__main__":
    asyncio.run(main())  # Запуск бота


