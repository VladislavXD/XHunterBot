from flask import Flask, redirect, request
from threading import Thread
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Ограничение по IP по умолчанию
limiter = Limiter(app=app, key_func=get_remote_address)

def get_id():
    return request.args.get('user_id', request.remote_addr)  # Если нет user_id, ограничиваем по IP



@app.route('/')
@limiter.limit("15 per minute", key_func=get_id)
def index():
    return "Бот живой"




@app.route('/r/<user_id>')
@limiter.limit("5 per minute", key_func=lambda: request.view_args['user_id'])  # Ограничиваем по user_id в URL
def open_external_browser(user_id):
    user_agent = request.headers.get('User-Agent', '').lower()

    if 'android' in user_agent:
        intent_link = f"intent://super-game-bot.netlify.app/g/{user_id}#Intent;scheme=https;end;"
        return redirect(intent_link, code=302)

    web_link = f"https://super-game-bot.netlify.app/g/{user_id}"
    return redirect(web_link, code=302)




def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
