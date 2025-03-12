import asyncio
from create_bot import bot
import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
import os
from dotenv import load_dotenv  

load_dotenv()


ADMIN_ID = int(os.getenv('ADMIN_ID'))

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Запуск бота
