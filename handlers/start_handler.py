from create_bot import bot  
from middleware.middleware import check_subscription_decorator
from telebot import types
from handlers.state import UserState
from create_bot import db
from main import ADMIN_ID
from .setLanguage import *
from .buttons import back
from gtts import gTTS
language = 'en'


ADMIN_ID = int(ADMIN_ID)
# @bot.callback_query_handler(func=lambda call: call.data == 'chek')
# @check_subscription_decorator
# def chekBtnCall(call):
#     main(call.message)
    
    
    
    
    
    
# change language
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def select_language(call):
    language_code = call.data.split('_')[1]
    UserState.set_language(call.message.chat.id, language_code)

    # Отправляем подтверждение
    lang_messages = {
        'en': "Language updated to English!",
        'ru': "Язык изменен на русский!"
    }
    bot.answer_callback_query(call.id, lang_messages.get(language_code, "Language updated!"))

    # Возвращаем пользователя в главное меню
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


def main(message, page=1):
    UserState.waiting_for_ip[message.chat.id] = False
    UserState.wait_for_tts[message.chat.id] = {'wait_for_tts': False}
    language = UserState.get_language(message.chat.id)  
    
    buttons = [
        types.InlineKeyboardButton(get_text('camera_btn', language), callback_data='cameraHack'),
        types.InlineKeyboardButton('🤖 Chat GPT4', callback_data='gpt4'),
        types.InlineKeyboardButton(get_text('acountHack_btn', language), callback_data='accountHack'),
        types.InlineKeyboardButton(get_text('ip_btn', language), callback_data='ipHack'),
        types.InlineKeyboardButton(get_text('language_btn', language), callback_data='change_language'),
        types.InlineKeyboardButton(get_text('contacnt_btn', language), callback_data='me'),
        types.InlineKeyboardButton(get_text('cerate_bot_btn', language), callback_data='createBot'),
        types.InlineKeyboardButton('Text to speach', callback_data='tts'),
    ]
    if(message.chat.id == ADMIN_ID):
        buttons.append(
        types.InlineKeyboardButton('Statistics', callback_data='stat'),
        )


    buttons_per_page = 6 # Количество кнопок на странице
    total_pages = (len(buttons) + buttons_per_page - 1) // buttons_per_page  # Всего страниц
    
    # Ограничение страницы
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Разделяем кнопки по страницам
    start_index = (page - 1) * buttons_per_page
    end_index = start_index + buttons_per_page
    page_buttons = buttons[start_index:end_index]
    
    # Добавляем кнопки "Назад" и "Вперёд"
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(types.InlineKeyboardButton(f"⬅ {get_text('back_btn', language)}", callback_data=f"page_{page - 1}"))
    if page < total_pages:
        navigation_buttons.append(types.InlineKeyboardButton(get_text('pagination', language), callback_data=f"page_{page + 1}"))
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*page_buttons)
    if navigation_buttons:
        markup.add(*navigation_buttons)
    
    
    user_name = db.get_name(message.chat.id)
    img = open('./img/main.jpeg', 'rb')
    caption_text = get_text('main_menu_caption', language).format(id=message.chat.id, name=db.get_name(message.chat.id))
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media, reply_markup=markup)
    img.close()

    # Сохраняем текущую страницу пользователя
    UserState.user_data[message.chat.id] = {'main_message_id': message.message_id, 'current_page': page}


# Обработчик для переключения страниц
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def handle_pagination(call):
    page = int(call.data.split('_')[1])  # Извлекаем номер страницы
    bot.answer_callback_query(call.id)  # Убираем "крутилку" в Telegram
    main(call.message, page=page)




# contact with me
@bot.callback_query_handler(func=lambda call: call.data == 'tts')
def tts(call):
    language = UserState.get_language(call.message.chat.id)  
    
    img = open('./img/main.jpeg', 'rb') 
    media = types.InputMediaPhoto(media=img, caption=get_text('tts_page', language))
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    
    UserState.wait_for_tts[call.message.chat.id] = {'wait_for_tts': True}


@bot.message_handler(func=lambda message: UserState.wait_for_tts.get(message.chat.id, {}).get('wait_for_tts', False))
def message_for_me(message):
   
    
    text = message.text
    
    try:
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save("audio.mp3")
        bot.send_audio(chat_id=message.chat.id, audio=open('audio.mp3', 'rb'))
        
    except Exception as e: print(f"error {e}", reply_markup=back(message.chat.id))






# contact with me
@bot.callback_query_handler(func=lambda call: call.data == 'me')
def contact_me(call):
    language = UserState.get_language(call.message.chat.id)  
    
   
    
    
    img = open('./img/main.jpeg', 'rb') 
    media = types.InputMediaPhoto(media=img, caption=get_text('contactMe_page', language))
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    
    UserState.waiting_for_message[call.message.chat.id] = {'waiting_for_message': True}


    




# ADMIN panel
@bot.message_handler(func=lambda message: UserState.waiting_for_message.get(message.chat.id, {}).get('waiting_for_message', False))
def message_for_me(message):
   
    
    text = message.text
    
    try:
        bot.send_message(ADMIN_ID, f'ID: {message.chat.id}\nПользоветль: {message.from_user.first_name}\nСообщение: {text}')
        UserState.waiting_for_message[message.chat.id]['waiting_for_message'] = False
        bot.send_message(message.chat.id, '✅', reply_markup=back(message.chat.id))
    except Exception as e: print(f"error {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'stat')
def statistic(call):
    
    sub = db.main_sub()
    img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
    caption_text = f"users: {sub}"
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
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
        