import os
from functools import partial
from glob import glob
from pathlib import Path
from random import choice

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


def start(update: Update, context: CallbackContext):
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    context.bot.send_message(chat_id=chat_id, text='hello!')


def send_image(*args):
    try:
        chat_id = args[0]
        update = args[1]
        context = args[2]
    except IndexError:
        context = args[0]
        chat_id = context.job.context
    base_dir = Path(__file__).resolve().parent.parent.parent
    img_dir = Path.joinpath(base_dir, 'images')
    imgs = glob(f'{img_dir}/*[png|jpg]')
    img_for_send = choice(imgs)
    with open(img_for_send, 'rb') as f:
        context.bot.send_photo(chat_id=chat_id, photo=f)


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    img_repeat_interval = int(os.getenv('IMAGE_SEND_REPEAT_INTERVAL', 14400))
    bot = Updater(token=token, use_context=True)

    dp = bot.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("space", partial(send_image, chat_id)))

    jq = bot.job_queue

    jq.run_repeating(send_image, interval=img_repeat_interval, context=chat_id)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
