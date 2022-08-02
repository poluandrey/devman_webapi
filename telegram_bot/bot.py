import os
from glob import glob
from pathlib import Path
from random import choice

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=-1001365773650, text='hello!')


def send_image(*args):
    if isinstance(args[0], Update) and isinstance(args[1], CallbackContext):
        update = args[0]
        context = args[1]
    elif isinstance(args[0], CallbackContext):
        context = args[0]
    base_dir = Path(__file__).resolve().parent.parent.parent
    img_dir = Path.joinpath(base_dir, 'images')
    chat_id = -1001365773650
    imgs = glob(f'{img_dir}/*jpg')
    img_for_send = choice(imgs)
    context.bot.send_photo(chat_id=chat_id, photo=open(img_for_send, 'rb'))


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    img_repeat_interval = int(os.getenv('IMAGE_SEND_REPEAT_INTERVAL', 14400))
    bot = Updater(token=token, use_context=True)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("space", send_image))

    jq = bot.job_queue

    jq.run_repeating(send_image, interval=img_repeat_interval)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
