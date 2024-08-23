import logging
import telebot
import functools
from telebot import custom_filters
from telebot.types import BotCommandScopeAllPrivateChats, BotCommand, KeyboardButton, ReplyKeyboardMarkup
import dotenv
import os
from threading import Lock

from handlers.index import register_handlers
from utils.storage import StateFirebaseStorage
from constants.types import UIResponseFeedback

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# bot.remove_webhook() # This ensures that any previously set webhook is deleted.

_UNINITIALIZED = object()

def _singleton(func):
    lock = Lock()
    _value = _UNINITIALIZED
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        nonlocal _value
        if _value is _UNINITIALIZED:
            with lock:
                if _value is _UNINITIALIZED:
                    _value = func(*args, **kwargs)
        return _value
    return wrapped

@_singleton
def create_telebot(app=None):
    telebot.logger.setLevel(logging.INFO)
    bot = telebot.TeleBot(BOT_TOKEN, 
                          threaded=False, 
                          state_storage=StateFirebaseStorage(app=app))
    register_handlers(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.set_my_commands([
        BotCommand('start', 'Initialize the Are You Ok? bot'),
        BotCommand('send', 'Send the current conversation to the LLM'),
    ], scope=BotCommandScopeAllPrivateChats())
    return bot

