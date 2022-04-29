import requests
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, MessageEntity
import ast
from pyrogram.types.list import List
from database import *
from database import Db

def get_mdisk(link, user_id):
    url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
    api = Db.user_info(user_id)['api']
    param = {'token': api, 'link': link}
    res = requests.post(url, json=param)
    try:
        shareLink = res.json()
        link = shareLink["sharelink"]
        print(link)
    except:
        print(link, " is invalid")
    return link

def caption_ent(caption_entities):
    x = []
    string = str(caption_entities)
    res = ast.literal_eval(string)
    try:
        for i in res:
            print(i)

            if "url" in i:
                print("Url")
                x.append(
                    MessageEntity(type=i["type"], offset=i["offset"], length=i["length"], url=get_mdisk(i["url"])))
            elif "user" in i:
                print("user")
                x.append(MessageEntity(type=i["type"], offset=i["offset"], length=i["length"], url=i["user"]))
            else:
                print("others")
                x.append(MessageEntity(type=i["type"], offset=i["offset"], length=i["length"]))

        entities = List(x)
        
    except:
        entities = caption_entities
        
    return entities



def replace_mdisk_link(text, user_id):
    links = re.findall(r'https?://mdisk.me[^\s]+', text)
    for link in links:
        try:
            mdisk_link = get_mdisk(link, user_id)
            text = text.replace(link, mdisk_link)
        except:
            text = text.replace(link, text)

    return text

def get_reply_markup(message, user_id):
    reply_markup = message['reply_markup']
    buttsons = []
    for markup in reply_markup["inline_keyboard"]:
        print(markup)
        buttons = []
        for j in markup:
            text = j["text"]
            url = j["url"]
            # Skip Other Link From Buttons
            if 'mdisk.me' not in url:
                continue
            url = get_mdisk(url, user_id=user_id)
            button = InlineKeyboardButton(text, url=url)
            buttons.append(button)
        buttsons.append(buttons)
    reply_markup = InlineKeyboardMarkup(buttsons)

    return reply_markup

def replace_caption(caption, user_id):
    # if url in caption Except(mdisk, t.me)
    print('replace caption call')
    # links = re.findall('https?://[a-zA-Z0-9_]+\.[a-zA-Z]+', caption)
    # links = re.findall("https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", caption)
    urls = Find(caption)
    for url in urls:
        if ('mdisk' in url) or ('t.me' in url):
            continue
        caption = caption.replace(url, '')

    # replace channel tag
    channel_tags = re.findall('https?://t\.me/[a-zA-Z0-9_]+|https?://t\.me/\+[a-zA-Z0-9]+|https?://telegram\.me/[a-zA-Z0-9_]+|@[A-Za-z0-9_]+', caption)
    channel_link = Db.user_info(user_id=user_id)['channel_link']

    for channel_tag in channel_tags:
        caption = caption.replace(channel_tag, channel_link)

    return replace_mdisk_link(text=caption, user_id=user_id)

    # Todo
    # youtube link 

def Find(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

