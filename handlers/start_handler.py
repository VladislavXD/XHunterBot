from create_bot import bot  
from middleware.middleware import check_subscription_decorator
from telebot import types
from handlers.state import UserState
from create_bot import db
from main import ADMIN_ID

@bot.callback_query_handler(func=lambda call: call.data == 'chek')
@check_subscription_decorator
def chekBtnCall(call):
    main(call.message)
    
    
#'/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
@check_subscription_decorator
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('I agree', callback_data='yes')
    markup.add(item_1)
    db.add_user(message.chat.id, message.from_user.first_name)

    
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
    item_6 = types.InlineKeyboardButton('Statistics', callback_data='stat') 
    item_7 = types.InlineKeyboardButton('✉ contact me', callback_data='me') 
    

    
    markup.add(item_1, item_2, item_3, item_4, item_5, item_7)

    if(message.chat.id == ADMIN_ID): markup.add(item_6)

    user_name = db.get_name(message.chat.id)

    img = open('./img/main.jpeg', 'rb')
    caption_text = f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}"
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media, reply_markup=markup)
    
    # bot.send_photo(message.chat.id, img, caption=f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}", reply_markup=markup, parse_mode="Markdown")
    UserState.user_data[message.chat.id] = {'main_message_id': message.message_id}











# contact with me
@bot.callback_query_handler(func=lambda call: call.data == 'me')
def contact_me(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)
    
    
    img = open('./img/main.jpeg', 'rb') 
    media = types.InputMediaPhoto(media=img, caption='send me question\nесть вопрос? можешь написать его суда')
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()
    
    UserState.wait_for_message[call.message.chat.id] = {'waiting_for_token': True}


    




# ADMIN panel

@bot.message_handler(func=lambda message: UserState.wait_for_message.get(message.chat.id, {}).get('waiting_for_token', False))
def message_for_me(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)
    
    text = message.text
    
    try:
        bot.send_message(ADMIN_ID, f'ID: {message.chat.id}\nПользоветль: {message.from_user.first_name}\nСообщение: {text}')
        UserState.wait_for_message[message.chat.id]['waiting_for_token'] = False
        bot.send_message(message.chat.id, '✅', reply_markup=markup)
    except Exception as e: print(f"error {e}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'stat')
def statistic(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)
    
    sub = db.main_sub()
    img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
    caption_text = f"users: {sub}"
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()


@bot.message_handler(commands=['answer'])
def answer(message):
    if(message.chat.id == ADMIN_ID):
        commands_parts = message.text.split(' ')

        if (len(commands_parts) < 3):
            bot.send_message(message.chat.id, 'Укажите все аргументы, /answer id - message')
            return

        user_id = commands_parts[1]
        text = ' '.join(commands_parts[2:])
      
        try:
            bot.send_message(user_id, text)
        except Exception as e: 
            bot.send_message(message.chat.id, f'error {e}')
        