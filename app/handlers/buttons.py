from telebot import types
from .setLanguage import get_text
from .state import UserState
def back(id):
  language = UserState.get_language(id)  
  
  markup = types.InlineKeyboardMarkup(row_width=2)
    
  item_1 = types.InlineKeyboardButton(get_text('back_btn', language), callback_data='back')
  markup.add( item_1)
  return markup