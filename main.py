from create_bot import bot
import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
import os

ADMIN_ID = 610691463

if __name__ == "__main__":
    bot.infinity_polling()
    