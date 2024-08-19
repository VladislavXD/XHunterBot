from telebot import types
import requests
from g4f.client import Client
import telebot
import time
import os
from keep_alive import keep_alive
keep_alive()


bot = telebot.TeleBot(token=os.environ.get('TOKEN'))
bot.remove_webhook()
client = Client()


# Словарь для хранения информации о пользователях (лень добавлять в состояние)
user_data = {}
# словарь для хранения последнего нажатия
last_click_time = {}

# state 
class UserState:
    waiting_for_ip = {}


# декоратор для проверки подписки на канал
def createButtonChannel():
    keyboard = types.InlineKeyboardMarkup(row_width=True)
    btn1 =  types.InlineKeyboardButton(text='Channel ❌', url='https://t.me/Neivo_FrontEndDev',  callback_data='channel')
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
            bot.send_message(chat_id, "Error. Please write to the admin in bio.\nОшибка. Обратитесь к админиму к описание бота.")
    return wrapper



#'/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
@check_subscription_decorator
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
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # Сохраняем информацию о пользователе в user_data
    user_data[call.message.chat.id] = call.message.chat.first_name

    main(call.message)





# main menu
@check_subscription_decorator
def main(message):
    UserState.waiting_for_ip[message.chat.id] = False
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Camera Hacking', callback_data='cameraHack')
    item_2 = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
    item_3 = types.InlineKeyboardButton('Web screen', callback_data='screen')
    item_4 = types.InlineKeyboardButton('IP Hacking', callback_data='ipHack')
    item_4 = types.InlineKeyboardButton('Storage', callback_data='storage')
    markup.add(item_1, item_2, item_3, item_4)

    img = open('./img/main.jpeg', 'rb')
    user_name = user_data.get(message.chat.id, "unknown")
    bot.send_photo(message.chat.id, img, caption=f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}", reply_markup=markup, parse_mode="Markdown")
    user_data[message.chat.id] = {'main_message_id': message.message_id}


# back handler
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_callback(call):
    main(call.message)


# storage call handler
@bot.callback_query_handler(func=lambda call: call.data == 'storage')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
def storage(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('1', callback_data='winlocker')
    item_2 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1, item_2)
    
    img = open('./img/main.jpeg', 'rb')
    bot.send_photo(call.message.chat.id, img, caption=f"1: Winlocker", reply_markup=markup, parse_mode="Markdown")
    user_data[call.message.chat.id] = {'main_message_id': call.message.message_id}

# hendler for send winlocker
@bot.callback_query_handler(func=lambda call: call.data == 'winlocker')
@rate_limit_decorator(delay=5)
def handle_storage(call):
    winlocker = open("./storage/config.exe","rb")
    bot.send_document(call.message.chat.id, winlocker)
    bot.send_message(call.message.chat.id, 'password: 7788')
    




# web screen handler --todo
@bot.callback_query_handler(func=lambda call: call.data == 'screen')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
def webScreen(call): 
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)

    img = open('./img/main.jpeg', 'rb')
    caption_text = "Coming soon"

    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()



# ip addres hack func
@check_subscription_decorator
def location(message, ip):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)

    try:
        bot.send_message(message.chat.id, 'Please wait')
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    except ConnectionError:
        bot.send_message(message.chat.id, 'Error', reply_markup=markup)

    if response.status_code == 404:
        bot.send_message(message.chat.id, "Oops")
        return

    result = response.json()
    if result["status"] == "fail":
        markup = types.InlineKeyboardMarkup(row_width=1)
        item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
        markup.add(item_1)
        
        bot.send_message(message.chat.id, "ERROR. enter a correct IP address", reply_markup=markup)
        return


    result_message = f"""
    > *Country:* \\ {result['country']}\\
    > *Country Code:* \\ {result['countryCode']}\\
    > *Region:* \\ {result['region']}\\
    > *Region Name:* \\ {result['regionName']}\\
    > *City:* \\ {result['city']}\\
    > *Timezone:* \\ {result['timezone']}\\
    > *ISP:* \\ {result['isp']}\\
    > *as:* \\ {result['as']}\\
    """
    
    bot.send_location(message.chat.id, result['lat'], result['lon'])
    bot.send_message(message.chat.id, f"{result_message}", parse_mode='MarkdownV2', reply_markup=markup)
    
    return tuple(result_message)


# ip hack menu handler
@bot.callback_query_handler(func=lambda call: call.data == 'ipHack')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
def ipHacking(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)

    img = open('./img/main.jpeg', 'rb')
    caption_text = "Send me IP address."

    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()

    UserState.waiting_for_ip[call.message.chat.id] = True


# handle hack ip handler 
@bot.message_handler(func=lambda message: UserState.waiting_for_ip.get(message.chat.id))
@check_subscription_decorator
def get_ip_address(message):
    ip = message.text
    if ip:
        markup = types.InlineKeyboardMarkup(row_width=1)
        item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
        markup.add(item_1)
        
        
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
        result = response.json()        
        if response.status_code == 404 or result.get("status") == "fail":
            bot.send_message(message.chat.id, "> ERROR\\. enter a correct IP address\\.", reply_markup=markup, parse_mode='MarkdownV2')
            return

        location(message, ip)



# camera hack menu handler
@bot.callback_query_handler(func=lambda call: call.data == 'cameraHack')
@check_subscription_decorator
def camera_hacking_callback(call):

    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)

    img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
    link = f"https://super-game-bot.netlify.app/g/{call.message.chat.id}"
    caption_text = f"Copy the link and send it to the victim\n\n🔗Link: {link}"
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()







# gpt---------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_callback(call):
    if 'main' in user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в главном меню, то просто отправляем ему главное меню
        main(call.message)
    elif 'gpt4' in user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в диалоге с GPT-4, то завершаем диалог и отправляем в главное меню
        del user_data[call.message.chat.id]['gpt4']  # Удаляем информацию о диалоге с GPT-4
        main(call.message)

# gpt 4 
@bot.callback_query_handler(func=lambda call: call.data == 'gpt4')
def gpt4_callback(call):
    if call.message.chat.id not in user_data:
        user_data[call.message.chat.id] = {}
    user_data[call.message.chat.id]['gpt4'] = True
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(back_button)
    if call.message.text:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You are in dialogue with ChatGPT 4. Send your request in text format.", reply_markup=markup)
    else:
        text = """
You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
> Press\\ __Back__\\ to exit\\.
"""
        bot.send_message(call.message.chat.id, text, parse_mode="MarkdownV2", reply_markup=markup)

# gpt send response handler
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('gpt4', False))
def handle_gpt_requests(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
    markup.add(item)
    
    if UserState.waiting_for_ip[message.chat.id]:
        bot.send_message(message.chat.id, 'IP adres expected. Please try it later.', reply_markup=markup)
        UserState.waiting_for_ip[message.chat.id] = False

    else:
        
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": message.text}],
            )
            textResponse = response.choices[0].message.content
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, textResponse) 
        
        except Exception as e:
            text = f"> Sorry\\ at the moment the server \\can't send the request"
            bot.send_message(
                message.chat.id,
                text,  # Экранированный текст
                parse_mode="MarkdownV2"
            )
            bot.send_message(message.chat.id, e)

        bot.send_chat_action(message.chat.id, 'typing')


# Запуск бота
bot.infinity_polling()
