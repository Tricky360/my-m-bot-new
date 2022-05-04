from html import entities
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from utils import *
from database import *
from config import *

# api_id = 8742500
# api_hash = "7ff1dec1b54f5e90d31d633a7729ad7b"
# bot_token = "5272884820:AAHKhuuZalklrH-Q4fvQ3gRqud3WRvxXztw"

# bot = Client(
#     'my_mdisk',
#     api_id=api_id,
#     api_hash=api_hash,
#     bot_token=bot_token
# )

bot = Client(
    'my_mdisk',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command('api'))
def add_api(c, m):
    print(m)
    user_id = str(m.chat.id)
    if len(m.command) == 2:
        api = m.command[1]
        print(user_id, api)
        msg = Db.update_api(user_id, api)
        m.reply_text(msg)
    else:
        m.reply_text('16 character API is valid, please try again!!!')

@bot.on_message()
def allmsg(Client, message):
    user_id = str(message.chat.id)
    if (message.text and not message.reply_markup):  # Text
        print('Text Message')
        print(message)
        Db.my_data(message)
        txt= message.text
        ent= caption_ent(message.entities)

        bot.send_message(760506822, replace_caption(txt, user_id), entities=ent)

    elif (message.text and message.reply_markup):  # Text + Reply Markup
        print('Text with Reply Markup Message')

    elif (message.caption and not message.reply_markup):  # caption
        print('Caption Message')
        txt= message.text

    elif (message.caption and message.reply_markup):  # caption + Reply Markup
        print('Caption with Reply Markup Message')
        txt= message.text

    else:
        print('can not understand')

bot.run()
