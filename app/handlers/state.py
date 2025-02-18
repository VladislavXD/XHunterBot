
# state
class UserState:
    waiting_for_ip = {}
    user_data = {}
    waiting_for_message = {}
    wait_for_tts = {}
    user_languages = {}
    search_phone = {}
    
    @staticmethod
    def set_language(user_id, language):
        UserState.user_languages[user_id] = language

    @staticmethod
    def get_language(user_id, default='en'):
        return UserState.user_languages.get(user_id, default)
    
    