import logging
from telebot.storage.base_storage import StateStorageBase
from firebase_admin import firestore

logger = logging.getLogger(__name__)

class StateFirebaseStorage(StateStorageBase):
    def __init__(self, app=None):
        self.firestore = firestore.client(app=app)
    
    def _get_data_document(self, chat_id, user_id):
        return self.firestore.collection("telegram_bot_storage_data").document(f"{chat_id}_{user_id}")
    
    def _get_state_document(self, chat_id, user_id):
        return self.firestore.collection("telegram_bot_storage_state").document(f"{chat_id}_{user_id}")
    
    def set_data(self, chat_id, user_id, key, value):
        doc = self._get_data_document(chat_id, user_id)
        if not doc.get().exists:
            doc.set({key: value})
        else:
            doc.update({key: value})
        return True
    
    def get_data(self, chat_id, user_id):
        ret = self._get_data_document(chat_id, user_id).get()
        if ret.exists:
            return ret.to_dict()
        return {}
    
    def reset_data(self, chat_id, user_id):
        ret = self._get_data_document(chat_id, user_id).get().exists
        self._get_data_document(chat_id, user_id).delete()
        return ret
    
    # def get_interactive_data(self, chat_id, user_id):
    #     return StateContext(self, chat_id, user_id)
    
    def set_state(self, chat_id, user_id, state):
        if hasattr(state, 'name'):
            state = state.name
        self._get_state_document(chat_id, user_id).set({'state': state})
        return True
    
    def delete_state(self, chat_id, user_id):
        ret = self._get_state_document(chat_id, user_id).get()
        self._get_state_document(chat_id, user_id).delete()
        return ret
    
    def get_state(self, chat_id, user_id):
        ret = self._get_state_document(chat_id, user_id).get()
        if ret.exists:
            return ret.to_dict()['state']
        return None
    
    def save(self, chat_id, user_id, data):
        self._get_data_document(chat_id, user_id).set(data)
        return True
