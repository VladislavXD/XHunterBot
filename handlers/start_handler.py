from create_bot import bot
from middleware.middleware import check_subscription_decorator
from telebot import types
from handlers.state import UserState

#'/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
# @check_subscription_decorator
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('I agree', callback_data='yes')
    markup.add(item_1)

    img = open('./img/warrning.webp', 'rb')
    bot.send_photo(message.chat.id, img, caption=""" \n
        If you use this bot, you agree to be bound by our terms.
        This bot is for educational purposes only.
        I am not responsible for any illegal activities that may occur as a result of using this bot.
        If you use this bot, you do so at your own risk.\n
        """, reply_markup=markup)
    img.close()

# Обработчик проверки подписки на канал
@bot.callback_query_handler(func=lambda call: call.data == 'chek')
def handle_check_subscription(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    check_subscription_decorator(call.message)
    
# Обработчик для кнопки "Я Согласен(а)"
@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def warrning_callback(call):
    bot.answer_callback_query(call.id, "Thanks")
    # Сохраняем информацию о пользователе в user_data
    UserState.user_data[call.message.chat.id] = call.message.chat.first_name

    main(call.message)





# main menu

def main(message):
    UserState.waiting_for_ip[message.chat.id] = False
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('👨‍💻 Camera Hacking', callback_data='cameraHack')
    item_3 = types.InlineKeyboardButton('🚫 Account Hacking', callback_data='accountHack')
    item_2 = types.InlineKeyboardButton('🤖 Chat GPT4', callback_data='gpt4')
    item_4 = types.InlineKeyboardButton('📍 IP Hacking', callback_data='ipHack')
    item_5 = types.InlineKeyboardButton('Create Bot', callback_data='createBot')
    markup.add(item_1, item_2, item_3, item_4, item_5)

    img = open('./img/main.jpeg', 'rb')
    user_name = UserState.user_data.get(message.chat.id, "unknown")
    caption_text = f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}"
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media, reply_markup=markup)
    
    # bot.send_photo(message.chat.id, img, caption=f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}", reply_markup=markup, parse_mode="Markdown")
    UserState.user_data[message.chat.id] = {'main_message_id': message.message_id}

