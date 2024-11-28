import sqlite3
import threading

class Database:
  def __init__(self, db_file):
    self.connection = sqlite3.connect(db_file, check_same_thread=False)
    self.lock = threading.Lock()
    
    
    
  
  def add_user(self, user_id, user_name):
    with self.lock:
        cursor = self.connection.cursor()
        # Проверяем, существует ли пользователь
        result = cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone()
        self.connection.commit()
        # Если пользователя нет, добавляем его
        if result is None:
            cursor.execute("INSERT INTO 'users' ('id', 'name') VALUES (?, ?)", (user_id, user_name,))
            self.connection.commit()
            

  def get_name(self, user_id):
    with self.lock:
      cursor = self.connection.cursor()
      result = cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
      if result[0]:
        return result[0]
      else:
        return 
    
    
  def subscribe(self, user_id):
    with self.lock:
      cursor = self.connection.cursor()
      cursor.execute("UPDATE users SET subscribers = subscribers + 1 WHERE id = ?", (user_id, ))
      self.connection.commit()
      
      
  def get_subscribe(self, user_id):
    with self.lock:
      cursor = self.connection.cursor()
      result = cursor.execute("SELECT subscribers FROM users WHERE id = ?", (user_id,)).fetchone()

      return result[0]
    
  def set_token(self, user_id, token):
    with self.lock:
      cursor = self.connection.cursor()
      cursor.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id, ))
      self.connection.commit()
      
  
  def get_token(self, user_id):
    with self.lock:
      cursor = self.connection.cursor()
      result = cursor.execute("SELECT token FROM users WHERE id = ?", (user_id,)).fetchone()

      return result[0]
    
    
    def main_sub(self):
      with self.lock:
        cursor = self.connection.cursor()
        result = cursor.execute("SELECT * FROM users", (user_id,)).fetchall()

        return len(result)
    
  # def get_all_bot_tokens(self):
  #   result = self.cursor.execute('''
  #       SELECT token FROM users
  #   ''').fetchall()
  #   print(result[0][0])
  #   return result[0][0]
  
  