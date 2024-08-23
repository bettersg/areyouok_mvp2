from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from constants.types import UIResponseFeedback


def send_message(message, bot: TeleBot):
  msg = bot.reply_to(message, "Hey there, great to meet you. I’m RUOK bot, your personal peer support companion to provide all the resources you may need to provide assistance to your loved one in emotional distress. We provide conversation suggestions, resources on peer support best practices, and a directory of mental health services in Singapore.\n\nHow can I help you?")

# Note: this function doesn't register itself to the next step handler, so it's only called once.
def handle_feedback(message, bot: TeleBot):
  if message.text == UIResponseFeedback.YES.value:
    bot.reply_to(message, "I'm glad to hear that! If you need any help, feel free to ask me anything.")
  elif message.text == UIResponseFeedback.NO.value:
    bot.reply_to(message, "Oh no, could you tell me even more then?")
  else:
    bot.reply_to(message, "Unrecognized callback data")

# General message handler
def handle_message(message, bot: TeleBot):
  markup = ReplyKeyboardMarkup(one_time_keyboard=True)
  markup.add(
    KeyboardButton(UIResponseFeedback.YES.value),
    KeyboardButton(UIResponseFeedback.NO.value),
  )
  reply = bot.reply_to(message, "Oh I so get you. Do tell me more!\n\nDoes this help?", reply_markup=markup) # Placeholder message
  bot.register_next_step_handler(reply, handle_feedback)

def register_handlers(bot: TeleBot):
  bot.register_message_handler(handle_message, pass_bot=True,)
  bot.register_message_handler(send_message, pass_bot=True, commands=['start'])

