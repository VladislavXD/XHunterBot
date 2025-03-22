from flask import Flask, redirect, request
from threading import Thread
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)

# Привязываем Limiter к Flask-приложению

limiter = Limiter(app=app, key_func=get_remote_address) # Используем get_remote_address в качестве key_func

def get_id():
    return request.args.get('user_id', request.remote_addr)  # Если нет user_id, ограничиваем по IP

# Основной обработчик
@app.route('/')
@limiter.limit("15 per minute", key_func=get_id)
def index():
    
    return "Бот живой"
  
  
  
# Редирект на внешний URL с передачей user_id для получения данных о пользователе
@app.route('/r/<user_id>')
@limiter.limit("5 per minute", key_func=get_id)
def open_external_browser(user_id):
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Если Android — используем intent-ссылку
    if 'android' in user_agent:
        intent_link = f"intent://super-game-bot.netlify.app/g/{user_id}#Intent;scheme=https;end;"
        return redirect(intent_link, code=302)
    
    # Для ПК и iOS — обычный редирект
    web_link = f"https://super-game-bot.netlify.app/g/{user_id}"
    return redirect(web_link, code=302)


# Запуск веб-сервера
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
    
keep_alive()