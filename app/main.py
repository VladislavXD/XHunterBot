import asyncio
from create_bot import bot
import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
import os

ADMIN_ID = os.environ['ADMIN_ID']

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Запуск бота
