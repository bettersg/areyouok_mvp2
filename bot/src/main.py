import telebot
from telebot import types
import dotenv
import os
from enum import Enum

from constants.types import UIResponseFeedback

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# bot.remove_webhook() # This ensures that any previously set webhook is deleted.

@bot.message_handler(commands=['start', 'help'])
def send_message(message):
  msg = bot.reply_to(message, "Hey there, great to meet you. I’m RUOK bot, your personal peer support companion to provide all the resources you may need to provide assistance to your loved one in emotional distress. We provide conversation suggestions, resources on peer support best practices, and a directory of mental health services in Singapore.\n\nHow can I help you?")

# Note: this function doesn't register itself to the next step handler, so it's only called once.
def handle_feedback(message):
  if message.text == UIResponseFeedback.YES.value:
    bot.reply_to(message, "I'm glad to hear that! If you need any help, feel free to ask me anything.")
  elif message.text == UIResponseFeedback.NO.value:
    bot.reply_to(message, "Oh no, could you tell me even more then?")
  else:
    bot.reply_to(message, "Unrecognized callback data")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  markup.add(
    types.KeyboardButton(UIResponseFeedback.YES.value),
    types.KeyboardButton(UIResponseFeedback.NO.value),
  )
  reply = bot.reply_to(message, "Oh I so get you. Do tell me more!\n\nDoes this help?", reply_markup=markup) # Placeholder message
  bot.register_next_step_handler(reply, handle_feedback)


print("Bot started")
bot.infinity_polling()