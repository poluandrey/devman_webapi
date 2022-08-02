# This project provides several options
1. upload images via SpaceX API
2. upload images via NASA API
3. launch a telegram bot that will post images

## .env
* NASA_WEB_TOKEN - token for working with NASA API
* TELEGRAM_TOKEN - token for working with Telegram API
* IMAGE_SEND_REPEAT_INTERVAL - interval in seconds for posting an image to a channel. Default values 4 hours

## Start working
### download images
get help message

``python main.py --help``

### run telegram bot
``python telegram_bot/bot.py``
