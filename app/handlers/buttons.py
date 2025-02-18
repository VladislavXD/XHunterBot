from telebot import types
from .setLanguage import get_text
from .state import UserState
def back(id):
  language = UserState.get_language(id)  
  
  markup = types.InlineKeyboardMarkup(row_width=2)
    
  item_1 = types.InlineKeyboardButton(get_text('back_btn', language), callback_data='back')
  markup.add( item_1)
  return markup

def cameraHackBtn(id):
  language = UserState.get_language(id)  
  
  markup = types.InlineKeyboardMarkup(row_width=1)
    
  item_1 = types.InlineKeyboardButton(get_text('cameraHackBtn', language), callback_data='hackLink')
  item_2 = types.InlineKeyboardButton(get_text('back_btn', language), callback_data='back')
  markup.add( item_1, item_2)
  return markup



