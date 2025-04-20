from create_bot import bot  
from middleware.middleware import check_subscription_decorator
from telebot import types
from handlers.state import UserState
from create_bot import db
from main import ADMIN_ID
from .setLanguage import *
from .buttons import back
from gtts import gTTS
import phonenumbers
from phonenumbers import geocoder, carrier, timezone


# from telethon.sync import TelegramClient
# from telethon.tl.functions.contacts import ImportContactsRequest, ResolveUsernameRequest
# from telethon.tl.types import InputPhoneContact


language = 'en'



# @bot.callback_query_handler(func=lambda call: call.data == 'chek')
# @check_subscription_decorator
# async def chekBtnCall(call):
#     main(call.message)
    
    
api_id = "28823899"
api_hash = "a51f06f49eb49a38def93795881286b9"

# TODO: Подключить Telethon для поиска пользователей
# client = TelegramClient("my_session", api_id, api_hash)
# client.start()
 

# async def find_by_phone(phone_number):
#     """ 🔍 Поиск пользователя по номеру телефона """
#     contact = InputPhoneContact(client_id=0, phone=phone_number, first_name="Temp", last_name="Contact")
#     result = await client(ImportContactsRequest([contact]))

#     user = result.users[0] if result.users else None
#     return user


# async def find_by_username(username):
#     """ 🔍 Поиск пользователя по username """
#     try:
#         result = await client(ResolveUsernameRequest(username.strip("@")))
#         return result.users[0] if result.users else None
#     except Exception:
#         return None


# async def find_by_id(user_id):
#     """ 🔍 Поиск пользователя по Telegram ID """
#     try:
#         return await client.get_entity(user_id)
#     except Exception:
#         return None


# def format_user_info(user):
#     """ 📌 Форматирование информации о пользователе """
#     if not user:
#         return "❌ Пользователь не найден!"

#     return (
#         f"✅ Пользователь найден!\n"
#         f"🔹 Telegram ID: `{user.id}`\n"
#         f"🔹 Username: @{user.username if user.username else 'Нет'}\n"
#         f"🔹 Имя: {user.first_name if user.first_name else 'Нет'}\n"
#         f"🔹 Фамилия: {user.last_name if user.last_name else 'Нет'}"
#     )






def lookup_phone_number(phone):
    """ 🔍 Поиск максимума данных о номере телефона """
    try:
        number = phonenumbers.parse(phone)

        # Проверяем валидность номера
        if not phonenumbers.is_possible_number(number):
            return "❌ Ошибка: Номер не является возможным (слишком короткий/длинный)"
        if not phonenumbers.is_valid_number(number):
            return "❌ Ошибка: Номер невалидный (не зарегистрирован в сети)"

        # Получаем данные
        country = geocoder.description_for_number(number, "ru")  # Страна
        operator = carrier.name_for_number(number, "ru")  # Оператор
        timezones = timezone.time_zones_for_number(number)  # Часовой пояс
        number_type = phonenumbers.number_type(number)

        # Определяем тип номера
        type_mapping = {
            0: "Неизвестный",
            1: "Фиксированный (городской) номер",
            2: "Мобильный номер",
            3: "Пейджер",
            4: "VoIP (интернет-телефония)",
            5: "Личный номер",
            6: "Универсальный доступ",
            7: "Корпоративный номер"
        }
        number_type_str = type_mapping.get(number_type, "Неизвестный")

        # Формируем ответ
        info = f"""
📱 **Номер:** {phone}
🌍 **Страна:** {country}
📡 **Оператор:** {operator if operator else 'Неизвестен'}
⏰ **Часовой пояс:** {', '.join(timezones)}
ℹ **Тип номера:** {number_type_str}
✅ **Номер действительный:** {'Да' if phonenumbers.is_valid_number(number) else 'Нет'}
"""
        return info.strip()
    except phonenumbers.NumberParseException:
        return "❌ Ошибка: Некорректный номер телефона"



    
# change language
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
async def select_language(call):
    language_code = call.data.split('_')[1]
    UserState.set_language(call.message.chat.id, language_code)

    # Отправляем подтверждение
    lang_messages = {
        'en': "Language updated to English!",
        'ru': "Язык изменен на русский!",
        'uz': "Til o'zgartirildi!"
    }
    await bot.answer_callback_query(call.id, lang_messages.get(language_code, "Language updated!"))

    # Возвращаем пользователя в главное меню
    await main(call.message)




#'/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
@check_subscription_decorator
async def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('I agree', callback_data='yes')
    markup.add(item_1)
    
    language = UserState.get_language(message.chat.id)  
    

    
    await db.add_user(message.chat.id, message.from_user.first_name)

    
    img = open('./img/warrning.webp', 'rb')
    await bot.send_photo(message.chat.id, img, caption=f""" \n{get_text('warrning', language)}\n
        """, reply_markup=markup)
    img.close()
    

# Обработчик проверки подписки на канал
@bot.callback_query_handler(func=lambda call: call.data == 'chek')
async def handle_check_subscription(call):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    check_subscription_decorator(call.message)
    
# Обработчик для кнопки "Я Согласен(а)"
@bot.callback_query_handler(func=lambda call: call.data == 'yes')
async def warrning_callback(call):
    language = UserState.get_language(call.message.chat.id)
    
    await bot.answer_callback_query(call.id, get_text('thanks', language))
    # Сохраняем информацию о пользователе в user_data
    UserState.user_data[call.message.chat.id] = call.message.chat.first_name

    await main(call.message)





# main menu


async def main(message, page=1):
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
        types.InlineKeyboardButton('Text to speach', callback_data='tts'),
        types.InlineKeyboardButton(get_text('searchPhone_btn', language), callback_data='search_phone'),
        types.InlineKeyboardButton(get_text('searchUser_btn', language), callback_data='search_user'),
        types.InlineKeyboardButton(get_text('cerate_bot_btn', language), callback_data='createBot'),
        
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
    
    
    user_name = await db.get_name(message.chat.id)
    img = open('./img/main.jpeg', 'rb')
    caption_text = get_text('main_menu_caption', language).format(id=message.chat.id, name=user_name)
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    await bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media, reply_markup=markup)
    img.close()

    # Сохраняем текущую страницу пользователя
    UserState.user_data[message.chat.id] = {'main_message_id': message.message_id, 'current_page': page}




@bot.callback_query_handler(func=lambda call: call.data == 'search_user')
async def search_user(call):
    """ 📩 Просим пользователя отправить данные для поиска пользователя """

    language = UserState.get_language(call.message.chat.id)
    img = open('./img/main.jpeg', 'rb')
    media = types.InputMediaPhoto(media=img, caption=get_text('search_user', language))
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    



# TODO Перенести обработчики в отдельные файлы
@bot.callback_query_handler(func=lambda call: call.data == 'search_phone')
async def user_id(call):
    """ 📩 Просим пользователя отправить данные для поиска """
    language = UserState.get_language(call.message.chat.id)
    img = open('./img/main.jpeg', 'rb')
    media = types.InputMediaPhoto(media=img, caption=get_text('phone_user', language))
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    
    # Ожидаем следующий ввод от пользователя
    UserState.search_phone[call.message.chat.id] = {'search_phone': True}


@bot.message_handler(func=lambda message: UserState.search_phone.get(message.chat.id, {}).get('search_phone', False))
async def process_search(message):
    """ 🔍 Обрабатываем поиск номера телефона """
    phone = message.text.strip()
    response = lookup_phone_number(phone)
    await bot.send_message(message.chat.id, response, parse_mode="Markdown" )

    # Сбрасываем состояние
    UserState.search_phone[message.chat.id]['search_phone'] = False



    
    
# Обработчик для переключения страниц
@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
async def handle_pagination(call):
    page = int(call.data.split('_')[1])  # Извлекаем номер страницы
    await bot.answer_callback_query(call.id)  # Убираем "крутилку" в Telegram
    await main(call.message, page=page)




# contact with me
@bot.callback_query_handler(func=lambda call: call.data == 'tts')
async def tts(call):
    language = UserState.get_language(call.message.chat.id)  
    
    img = open('./img/main.jpeg', 'rb') 
    media = types.InputMediaPhoto(media=img, caption=get_text('tts_page', language))
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    
    UserState.wait_for_tts[call.message.chat.id] = {'wait_for_tts': True}


@bot.message_handler(func=lambda message: UserState.wait_for_tts.get(message.chat.id, {}).get('wait_for_tts', False))
async def message_for_me(message):
   
    
    text = message.text
    
    try:
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save("audio.mp3")
        await bot.send_audio(chat_id=message.chat.id, audio=open('audio.mp3', 'rb'))
        
    except Exception as e: print(f"error {e}", reply_markup=back(message.chat.id))






# contact with me
@bot.callback_query_handler(func=lambda call: call.data == 'me')
async def contact_me(call):
    language = UserState.get_language(call.message.chat.id)  
    
   
    
    
    img = open('./img/main.jpeg', 'rb') 
    media = types.InputMediaPhoto(media=img, caption=get_text('contactMe_page', language))
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()
    
    UserState.waiting_for_message[call.message.chat.id] = {'waiting_for_message': True}


    




# ADMIN panel
@bot.message_handler(func=lambda message: UserState.waiting_for_message.get(message.chat.id, {}).get('waiting_for_message', False))
async def message_for_me(message):
   
    
    text = message.text
    
    try:
        await bot.send_message(ADMIN_ID, f'ID: {message.chat.id}\nПользоветль: {message.from_user.first_name}\nСообщение: {text}')
        UserState.waiting_for_message[message.chat.id]['waiting_for_message'] = False
        await bot.send_message(message.chat.id, '✅', reply_markup=back(message.chat.id))
    except Exception as e: print(f"error {e}")


@bot.callback_query_handler(func=lambda call: call.data == 'stat')
async def statistic(call):
    
    sub = await db.main_sub()
    img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
    caption_text = f"users: {sub}"
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()


@bot.message_handler(commands=['answer'])
async def answer(message):
    print('конманда вызвана')
    if(message.chat.id == ADMIN_ID):
        commands_parts = message.text.split(' ')

        if (len(commands_parts) < 3):
            await bot.send_message(message.chat.id, 'Укажите все аргументы, /answer id - message')
            return

        user_id = int(commands_parts[1])
        text = ' '.join(commands_parts[2:])
      
        try:
            await bot.send_message(user_id, text)
        except Exception as e: 
            await bot.send_message(message.chat.id, f'error {e}')
        