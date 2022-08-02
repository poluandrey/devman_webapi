import os
import logging

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from dotenv import load_dotenv


def start(update: Update, context: CallbackContext):
    print(update)
    msg = update.channel_post
    print(msg)
    context.bot.send_message(chat_id=-1001365773650, text='hello!')


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    bot = Updater(token=token, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", start))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()


