from flask import Flask, redirect
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    
    return "Бот живой"
  
@app.route('/redirect/<user_id>')
def open_external_browser(user_id):
    # Android Intent-ссылка
    intent_link = f"intent://super-game-bot.netlify.app/g/{user_id}#Intent;scheme=https;package=com.android.chrome;end;"
    
    return redirect(intent_link, code=302)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()