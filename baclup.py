
# import telebot
# from telebot import types
# import requests
# from g4f.client import Client
# from telebot import apihelper

# # apihelper.proxy = {'http': 'http://proxy.server:3128', 'https': 'http://proxy.server:3128'}
# # proxies = {
# #     'http': 'http://proxy.server:3128',
# #     'https': 'http://proxy.server:3128'
# # }
# API_TOKEN = '7090605003:AAGyGnfwrqkm_L99ourmXr8f4Yp3uUlk_Qc'

# bot = telebot.TeleBot(API_TOKEN)
# client = Client()
# # Словарь для хранения информации о пользователях
# user_data = {}

# class UserState:
#     waiting_for_ip = {}







# def createButtonChannel():
#     keyboard = types.InlineKeyboardMarkup(row_width=True)
#     btn1 =  types.InlineKeyboardButton(text='Канал ❌', url='https://t.me/Neivo_FrontEndDev',  callback_data='channel')
#     btn2 = types.InlineKeyboardButton(text='Проверить', callback_data='chek')
#     keyboard.add(btn1, btn2)
#     return keyboard




# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def check_subscription(call):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_1 = types.InlineKeyboardButton('Я Согласен(а)', callback_data='yes')
#     markup.add(item_1)

#     try:
#         member = bot.get_chat_member(chat_id='-1001832025300', user_id=call.chat.id)
#         if member.status in ['member', 'administrator', 'creator']:
#             img = open('./img/warrning.webp', 'rb')
#             bot.send_photo(call.chat.id, img, caption=""" \n
#                 If you use this bot, you agree to be bound by our terms.
#                 This bot is for educational purposes only.
#                 I am not responsible for any illegal activities that may occur as a result of using this bot.
#                 If you use this bot, you do so at your own risk.\n
#                 """, reply_markup=markup)
#             img.close()
#         else:
#             bot.send_message(call.chat.id, "Вы не подписаны на канал! Подпишитесь и повторите попытку.", reply_markup=createButtonChannel())
#     except Exception as e:
#         bot.send_message(call.chat.id, "Не удалось проверить подписку. Пожалуйста, убедитесь, что канал доступен.")
  

# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.data == 'chek':
#         bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
#         check_subscription(call.message)
#     elif call.data == 'yes':
        

# # Обработчик для кнопки "Я Согласен(а)"
# def warrning_callback(call):
#     bot.answer_callback_query(call.id, "Thanks")
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     # Сохраняем информацию о пользователе в user_data
#     user_data[call.message.chat.id] = call.message.chat.first_name

#     main(call.message)





# # Главное меню
# def main(message):
#     UserState.waiting_for_ip[message.chat.id] = False
    
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_1 = types.InlineKeyboardButton('Camera Hacking', callback_data='cameraHack')
#     item_2 = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
#     item_3 = types.InlineKeyboardButton('Web screen', callback_data='screen')
#     item_4 = types.InlineKeyboardButton('IP Hacking', callback_data='ipHack')
#     markup.add(item_1, item_2, item_3, item_4)

#     img = open('./img/main.jpeg', 'rb')
#     user_name = user_data.get(message.chat.id, "Unknown")
#     bot.send_photo(message.chat.id, img, caption=f"Main menu\n\n🆔 Your id: `{message.chat.id}`\n👤 Your name: {user_name}", reply_markup=markup, parse_mode="Markdown")
#     user_data[message.chat.id] = {'main_message_id': message.message_id}




# @bot.callback_query_handler(func=lambda call: call.data == 'screen')
# def webScreen(call): 
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     item_1 = types.InlineKeyboardButton('Back', callback_data='back')
#     markup.add(item_1)

#     img = open('./img/main.jpeg', 'rb')
#     caption_text = "Coming soon"

#     media = types.InputMediaPhoto(media=img, caption=caption_text)
#     bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
#     img.close()



# # ip addres hack
# def location(message, ip):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     item_1 = types.InlineKeyboardButton('Back', callback_data='back')
#     markup.add(item_1)

#     try:
#         bot.send_message(message.chat.id, 'Please wait')
#         response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
#     except ConnectionError:
#         bot.send_message(message.chat.id, 'Error', reply_markup=markup)

#     if response.status_code == 404:
#         bot.send_message(message.chat.id, "Oops")
#         return

#     result = response.json()
#     if result["status"] == "fail":
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
#         markup.add(item_1)
        
#         bot.send_message(message.chat.id, "ERROR. enter a correct IP address", reply_markup=markup)
#         return


#     result_message = f"""
# > *Country:* \\ {result['country']}\\
# > *Country Code:* \\ {result['countryCode']}\\
# > *Region:* \\ {result['region']}\\
# > *Region Name:* \\ {result['regionName']}\\
# > *City:* \\ {result['city']}\\
# > *Timezone:* \\ {result['timezone']}\\
# > *ISP:* \\ {result['isp']}\\
# > *as:* \\ {result['as']}\\
# """
#     bot.send_location(message.chat.id, result['lat'], result['lon'])
#     bot.send_message(message.chat.id, f"{result_message}", parse_mode='MarkdownV2', reply_markup=markup)
    
#     return tuple(result_message)

# @bot.callback_query_handler(func=lambda call: call.data == 'ipHack')
# def ipHacking(call):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     item_1 = types.InlineKeyboardButton('Back', callback_data='back')
#     markup.add(item_1)

#     img = open('./img/main.jpeg', 'rb')
#     caption_text = "Send me IP address."

#     media = types.InputMediaPhoto(media=img, caption=caption_text)
#     bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
#     img.close()

#     UserState.waiting_for_ip[call.message.chat.id] = True

# @bot.message_handler(func=lambda message: UserState.waiting_for_ip.get(message.chat.id))
# def get_ip_address(message):
#     ip = message.text
#     if ip:
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
#         markup.add(item_1)
        
        
#         response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
#         result = response.json()        
#         if response.status_code == 404 or result.get("status") == "fail":
#             bot.send_message(message.chat.id, "> ERROR\\. enter a correct IP address\\.", reply_markup=markup, parse_mode='MarkdownV2')
#             return

#         location(message, ip)



# @bot.callback_query_handler(func=lambda call: call.data == 'back')
# def back_callback(call):
#     main(call.message)

# #Меню взлома камеры
# @bot.callback_query_handler(func=lambda call: call.data == 'cameraHack')
# def camera_hacking_callback(call):

#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_1 = types.InlineKeyboardButton('Back', callback_data='back')
#     markup.add(item_1)

#     img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
#     link = f"https://super-game-bot.netlify.app/g/{call.message.chat.id}"
#     caption_text = f"Copy the link and send it to the victim\n\n🔗Link: {link}"
    
#     media = types.InputMediaPhoto(media=img, caption=caption_text)
#     bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
#     img.close()







#     # gpt---------------------------------------------------
# @bot.callback_query_handler(func=lambda call: call.data == 'back')
# def back_callback(call):
#     if 'main' in user_data.get(call.message.chat.id, {}):
#         # Если пользователь находится в главном меню, то просто отправляем ему главное меню
#         main(call.message)
#     elif 'gpt4' in user_data.get(call.message.chat.id, {}):
#         # Если пользователь находится в диалоге с GPT-4, то завершаем диалог и отправляем в главное меню
#         del user_data[call.message.chat.id]['gpt4']  # Удаляем информацию о диалоге с GPT-4
#         main(call.message)

# # gpt 4
# @bot.callback_query_handler(func=lambda call: call.data == 'gpt4')
# def gpt4_callback(call):
    
    
#     if call.message.chat.id not in user_data:
#         user_data[call.message.chat.id] = {}
#     user_data[call.message.chat.id]['gpt4'] = True
#     markup = types.InlineKeyboardMarkup()
#     back_button = types.InlineKeyboardButton('Back', callback_data='back')
#     markup.add(back_button)
#     if call.message.text:
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You are in dialogue with ChatGPT 4. Send your request in text format.", reply_markup=markup)
#     else:
#         text = """
# You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
# > Press\\ __Back__\\ to exit\\.
# """
#         bot.send_message(call.message.chat.id, text, parse_mode="MarkdownV2", reply_markup=markup)


# @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('gpt4', False))
# def handle_gpt_requests(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     item = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
#     markup.add(item)
    
#     if UserState.waiting_for_ip[message.chat.id]:
#         bot.send_message(message.chat.id, 'IP adres expected. Please try it later.', reply_markup=markup)
#         UserState.waiting_for_ip[message.chat.id] = False

#     else:
        
#         bot.send_chat_action(message.chat.id, 'typing')
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[{"role": "user", "content": message.text}],
#             )
#             textResponse = response.choices[0].message.content
#             bot.send_chat_action(message.chat.id, 'typing')
#             bot.send_message(message.chat.id, textResponse) 
        
#         except Exception as e:
#             text = f"> Sorry\\ at the moment the server \\can't send the request"
#             bot.send_message(
#                 message.chat.id,
#                 text,  # Экранированный текст
#                 parse_mode="MarkdownV2"
#             )
#             bot.send_message(message.chat.id, e)

#         bot.send_chat_action(message.chat.id, 'typing')


# # Запуск бота
# bot.infinity_polling()



