import sys
import time
import random
import sqlite3

#Telepot
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

#Clarafai
from clarifai.rest import ClarifaiApp
app = ClarifaiApp()
model = app.models.get('FashionTrainer')

#sqlite3
from dbhelper import DBHelper
db = DBHelper()

def handle(msg):
    db.setup()
    content_type, chat_type, chat_id = telepot.glance(msg)
    top_id = 0
    bottom_id = 0

    def run():
        if content_type == 'text':
            if msg['text'] == '/start':
                reply = 'Welcome'
                shuffle_reset_keys(reply)

            if msg['text'] == 'Reset':
                reset_photos()
                reply = 'Done!'
                shuffle_reset_keys(reply)

            if msg['text'] == 'Shuffle':
                results = get_photos()
                if results != False:
                    accept_reject_keys()
                else:
                    reply = 'Please add more clothes!'
                    shuffle_reset_keys(reply)

            if msg['text'] == 'Accept':
                accept()
                reply = 'Good Choice:)'
                shuffle_reset_keys(reply)

            if msg['text'] == 'Reject':
                reply = 'Rejected'
                shuffle_reset_keys(reply)
        else:
            file_id = bot.getFile(msg['photo'][1]['file_id'])
            add_photo(file_id)

    def reset_photos():
        db.reset_items(chat_id)

    def get_photos():
        results = db.get_items(chat_id)

        original_tops = []
        original_bottoms = []

        for column in results:
            if column[0] == 'tops':
                original_tops.append(column)
            else:
                original_bottoms.append(column)

        if original_tops == [] or original_bottoms == []:
            return False

        global top_id
        global bottom_id

        random_top = random.choice(original_tops)
        top_id = random_top[1]
        random_bottom = random.choice(original_bottoms)
        bottom_id = random_bottom[1]

        bot.sendPhoto(chat_id, top_id)
        bot.sendPhoto(chat_id, bottom_id)

    def accept():
        global top_id
        global bottom_id
        top_and_bottom = [top_id, bottom_id]
        for file_id in top_and_bottom:
            db.accept_items(chat_id, file_id)

    def add_photo(file_id):
        photo_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_id['file_path'])
        result = model.predict_by_url(url=photo_url)
        result = result['outputs'][-1]['data']['concepts'][0]['name']

        if result == 'short' or result == 'jeans' or result == 'skirt':
            clothes_type = 'bottoms'
        else:
            clothes_type = 'tops'

        db.add_item(clothes_type, result, chat_id, file_id['file_id'])
        reply = 'Added an item'
        shuffle_reset_keys(reply)

    def accept_reject_keys():
        bot.sendMessage(chat_id, 'Would you like this set of clothes?',
        reply_markup=ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Accept'), KeyboardButton(text='Reject')]
        ],
        resize_keyboard=True
        ))

    def shuffle_reset_keys(reply):
        bot.sendMessage(chat_id, reply,
        reply_markup=ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Shuffle'), KeyboardButton(text='Reset')]
        ],
        resize_keyboard=True
        ))

    run()

bot = telepot.Bot(token=TOKEN)
MessageLoop(bot, handle).run_forever()

bot.setWebhook("https://fashionerbot.herokuapp.com/" + TOKEN)

# Keep the program running.
while 1:
    time.sleep(10)
