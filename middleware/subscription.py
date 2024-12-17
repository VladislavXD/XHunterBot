from telebot import types
import time
from create_bot import bot

# словарь для хранения последнего нажатия
last_click_time = {}


# декоратор для проверки подписки на канал
def createButtonChannel():
    keyboard = types.InlineKeyboardMarkup(row_width=True)
    btn1 =  types.InlineKeyboardButton(text='Channel ❌', url='https://t.me/just_vladislavDev',  callback_data='channel')
    btn2 = types.InlineKeyboardButton(text='Chek', callback_data='chek')
    keyboard.add(btn1, btn2)
    return keyboard



# Декоратор для блокировки многократных нажатий
def rate_limit_decorator(delay=5):
    def decorator(func):
        def wrapper(call):
            user_id = call.from_user.id
            current_time = time.time()
            last_time = last_click_time.get(user_id, 0)

            if current_time - last_time < delay:
                bot.answer_callback_query(call.id, "Please wait")
                return

            last_click_time[user_id] = current_time
            return func(call)
        return wrapper
    return decorator
