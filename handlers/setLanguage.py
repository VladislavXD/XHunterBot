from telebot import types
from create_bot import bot

def language_selection_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
    ]
    markup.add(*buttons)
    return markup




def get_text(key, language):
    translations = {
        'start_message': {
            'en': "Welcome! Please select an option below:",
            'ru': "Добро пожаловать! Выберите один из вариантов ниже:"
        },
        'main_menu_caption': {
            'en': "Main menu\n\n🆔 Your ID: {id}\n👤 Your name: {name}",
            'ru': "Главное меню\n\n🆔 Ваш ID: {id}\n👤 Ваше имя: {name}"
        },
        'back_btn': {
            'en': 'Back',
            'ru': 'Назад'
        },
        'contacnt_btn': {
          'en': 'Contact to Developer',
          'ru': 'Связь с админом'
        },
        'camera_btn': {
          'en': '👨‍💻 Camera Hacking',
          'ru': '👨‍💻 Взломать камеру'
        },
        'ip_btn': {
          'en' : '📍 IP Hacking',
          'ru': '📍 Пробив по IP'
        },
        'cerate_bot_btn': {
            'en': 'Create bot',
            'ru': 'Создать бота'
        },
        'language_btn': {
            'en': '🌐 Language',
            'ru': '🌐 Язык'
        },
        'cameraHack_page': {
            'en': "Copy the link and send it to the victim\n\n🔗Link: {link}",
            'ru': 'Скопируйте ссылку и отправьте жертве \n\n🔗сслка: {link}'
        },
        'ipHack_page': {
            'en': 'Send me IP address',
            'ru': 'Отравьте сюда IP адрес'
        },
        'chatGpt_page': {
            'en': """You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
> Press\\ __Back__\\ to exit\\.
""",
            'ru': """Вы находитесь в диалоге с ChatGpt 4\\. Отправьте свой запрос в текстовом формате\\. 
> Нажмите\\ __Назад__\\ чтобы выйти\\."""
        },
        'acountHack_btn': {
            'en': '🚫 Phishing',
            'ru': '🚫 Фишинг'
        },
        'acountHack_page': {
            'en': 'Coming soon',
            'ru': 'Тут будет ваша ссылка'
        },
        'contactMe_page': {
            'en': 'send me question',
            'ru': 'есть вопрос? можешь написать его сюда'
        },
        'pagination': {
            'en': '➡️ Next',
            'ru': '➡️ Вперед'
        },
        'tts_page': {
            'en': 'Send me some text\n\n--click on back to leave this page',
            'ru': 'Отправьте мне текст\n\n--Нажмите back чтобы завершить'
            
        }
        
        
    }
    return translations.get(key, {}).get(language, key)




@bot.callback_query_handler(func=lambda call: call.data == 'change_language')
def change_language(call):
    
    markup = language_selection_keyboard()
    img = open('./img/main.jpeg', 'rb')
    caption_text = "Select your language / Выберите язык:"
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.id, media=media, reply_markup=markup)
    img.close()