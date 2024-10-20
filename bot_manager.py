from telebot import TeleBot

# Список токенов всех ботов
BOT_TOKENS = [
    'TOKEN_1',
    'TOKEN_2',
    # добавь все необходимые токены
]

# Словарь для хранения экземпляров ботов
bots = {token: TeleBot(token) for token in BOT_TOKENS}
