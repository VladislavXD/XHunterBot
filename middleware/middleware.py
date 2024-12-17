from create_bot import bot
from middleware.subscription import createButtonChannel
import time


# словарь для хранения последнего нажатия
last_click_time = {}





def check_subscription_decorator(func):
    def wrapper(*args, **kwargs):
        message = args[0]  # Первым аргументом всегда будет message или call
        if hasattr(message, 'chat'):
            chat_id = message.chat.id
        elif hasattr(message, 'message'):
            chat_id = message.message.chat.id
        else:
            chat_id = message.from_user.id

        try:
            member = bot.get_chat_member(chat_id='-1001832025300', user_id=chat_id)
            if member.status in ['member', 'administrator', 'creator']:
                return func(*args, **kwargs)
            else:
                bot.send_message(chat_id, "You are not subscribed to the channel ", reply_markup=createButtonChannel())
        except Exception as e:
            bot.send_message(chat_id, f"Error. Please write to the admin in bio.\nОшибка. Обратитесь к админу в описание бота.{e}")
    return wrapper
  
