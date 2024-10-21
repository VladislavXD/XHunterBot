from create_bot import bot
import handlers.main_handler
import handlers.start_handler
import handlers.create_bot.add_bot
from handlers.keep_alive import keep_alive

keep_alive()



if __name__ == "__main__":
    bot.infinity_polling()