import sqlite3


class Database:
  def __init__(self, db_file):
    self.connection = sqlite3.connect(db_file, check_same_thread=False)
    self.cursor = self.connection.cursor()
    
    
    
  
  def add_user(self, user_id, user_name):
    with self.connection:
        # Проверяем, существует ли пользователь
        result = self.cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone()

        # Если пользователя нет, добавляем его
        if result is None:
            self.cursor.execute("INSERT INTO 'users' ('id', 'name') VALUES (?, ?)", (user_id, user_name,))

  def get_name(self, user_id):
    with self.connection:
      result = self.cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
      return result[0]
    
    
  def subscribe(self, user_id):
    with self.connection:
      self.cursor.execute("UPDATE users SET subscribers = subscribers + 1 WHERE id = ?", (user_id, ))
      
  def get_subscribe(self, user_id):
    with self.connection:
      result = self.cursor.execute("SELECT subscribers FROM users WHERE id = ?", (user_id,)).fetchone()

      return result[0]
    
  def set_token(self, user_id, token):
    with self.connection:
      self.cursor.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id, ))
  
  def get_token(self, user_id):
    with self.connection:
      result = self.cursor.execute("SELECT token FROM users WHERE id = ?", (user_id,)).fetchone()

      return result[0]
    
    
  def get_all_bot_tokens(self):
    result = self.cursor.execute('''
        SELECT token FROM users
    ''').fetchall()
    print(result[0][0])
    return result[0][0]