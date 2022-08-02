import os
from glob import glob
import logging
from pathlib import Path

from random import choice
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from dotenv import load_dotenv


def start(update: Update, context: CallbackContext):
    print(update)
    msg = update.channel_post
    print(msg)
    context.bot.send_message(chat_id=-1001365773650, text='hello!')


def send_image(update: Update, context: CallbackContext):
    base_dir = Path(__file__).resolve().parent.parent.parent
    print(base_dir)
    img_dir = Path.joinpath(base_dir, 'images')
    chat_id = -1001365773650
    imgs = glob(f'{img_dir}/*jpg')
    img_for_send = choice(imgs)
    context.bot.send_photo(chat_id=chat_id, photo=open(img_for_send, 'rb'))


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    bot = Updater(token=token, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("space", send_image))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()


