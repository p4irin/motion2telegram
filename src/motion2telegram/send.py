import os
from telegram_notifier_bot import Notifier

def send(picture: str) -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    notifier = Notifier(token)
    notifier.send("Motion detected!", chat_id)
    notifier.send_photo(picture, chat_id)