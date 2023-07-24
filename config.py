import os
from logging import DEBUG, INFO, WARNING, ERROR

jsonfile = "./wohnen.json"
loglevel = INFO

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']

# set search parameters
min_rooms = 1
max_rooms = 2
max_rent = 600
# 0 = no wbs
# 1 = only wbs
# 2 = doesn't matter
wbs = 2

