from flask import Flask, redirect, request
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    
    return "Бот живой"
  
@app.route('/r/<user_id>')
def open_external_browser(user_id):
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Если Android — используем intent-ссылку
    if 'android' in user_agent:
        intent_link = f"intent://super-game-bot.netlify.app/g/{user_id}#Intent;scheme=https;end;"
        return redirect(intent_link, code=302)
    
    # Для ПК и iOS — обычный редирект
    web_link = f"https://super-game-bot.netlify.app/g/{user_id}"
    return redirect(web_link, code=302)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()