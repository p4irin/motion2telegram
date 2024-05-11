import os
import sys
from telegram_notifier_bot import Notifier

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
notifier = Notifier(token)
notifier.send("Motion detected!", chat_id)
notifier.send_photo(sys.argv[1], chat_id)