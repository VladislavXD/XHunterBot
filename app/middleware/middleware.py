from create_bot import bot
from middleware.subscription import createButtonChannel
import time


# словарь для хранения последнего нажатия
last_click_time = {}





def check_subscription_decorator(func):
    async def wrapper(*args, **kwargs):
        message = args[0]  # Первым аргументом всегда будет message или call
        if hasattr(message, 'chat'):
            chat_id = message.chat.id
        elif hasattr(message, 'message'):
            chat_id = message.message.chat.id
        else:
            chat_id = message.from_user.id

        try:
            member = await bot.get_chat_member(chat_id='-1001832025300', user_id=chat_id)
            if member.status in ['member', 'administrator', 'creator']:
                return await func(*args, **kwargs)
            else:
                await bot.send_message(chat_id, "You are not subscribed to the channel ", reply_markup=createButtonChannel())
        except Exception as e:
            await bot.send_message(chat_id, f"Error. Try again.\nОшибка. Поробуйте повторить.\n\n{e}")
    return wrapper
  


# def check_subscription_decorator(func):
#     from telebot.types import Message, CallbackQuery

#     async def wrapper(*args, **kwargs):
#         # Ищем объект message или call
#         message = None
#         user_id = None

#         for arg in args:
#             if isinstance(arg, Message):
#                 message = arg
#                 user_id = message.from_user.id
#                 break
#             elif isinstance(arg, CallbackQuery):
#                 message = arg.message
#                 user_id = arg.from_user.id
#                 break

#         if not user_id:
#             print("[Ошибка декоратора] Невозможно определить пользователя")
#             return

#         try:
#             member = await bot.get_chat_member(chat_id='-1001832025300', user_id=user_id)
#             if member.status in ['member', 'administrator', 'creator']:
#                 return await func(*args, **kwargs)
#             else:
#                 await bot.send_message(user_id, "Пожалуйста, подпишитесь на канал для продолжения.", reply_markup=createButtonChannel())
#         except Exception as e:
#             await bot.send_message(user_id, f"Ошибка при проверке подписки.\n\n{e}")
#             print(f"[Ошибка проверки подписки] user_id={user_id} — {e}")

#     return wrapper


