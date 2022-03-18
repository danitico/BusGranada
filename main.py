import os

from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import Message, ForceReply

from constants import WELCOME_MESSAGE, REQUEST_STOP_NUMBER
from services import StopService


load_dotenv()

bot = TeleBot(
    token=os.getenv("TELEGRAM_TOKEN")
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, WELCOME_MESSAGE)

@bot.message_handler(commands=['parada'])
def send_stop_information(message: Message):
    argv = message.text.split()

    if len(argv) == 1:
        bot.send_message(
            message.chat.id,
            REQUEST_STOP_NUMBER,
            reply_markup=ForceReply(selective=False)
        )
    elif len(argv) == 2:
        stop_number = argv[1]
        bot.reply_to(
            message,
            StopService.get_stop_information(stop_number)
        )

@bot.message_handler(regexp=r'^\d{1,4}$')
def get_number_and_send_stop_information(message: Message):
    stop_number = message.text

    bot.reply_to(
        message,
        StopService.get_stop_information(stop_number)
    )

bot.infinity_polling()
