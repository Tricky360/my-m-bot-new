import json
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient

from utils import *


class Db:
    cluster = MongoClient(
        'mongodb+srv://abc:1234@cluster0.pbs4y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

    db = cluster['dummy']
    collection = db['test']

    @classmethod
    def my_data(cls, msg):
        user_id = str(msg['chat']['id'])
        user_name = msg['chat']['first_name']
        join_date = msg['date']

        # If already user in database
        if Db.collection.find_one({'_id': user_id}):
            print("User in database")
            return True

        else:
            user_data = {
                        "_id": user_id,
                        'name': user_name, 
                        'date': join_date, 
                        'api': "", 
                        'channel_link': "",
                        }
            Db.collection.insert_one(user_data)
            print('user added succesfull')
            print(Db.collection.find_one({"_id": user_id}))
            return False

    @classmethod
    def user_info(cls, user_id):
        print(user_id, type(user_id))
        data = Db.collection.find_one({'_id': user_id})
        print(data)
        return data

    @classmethod
    def update_api(cls, user_id, new_api):
        res = Db.check_api_valid(api=new_api, l="https://mdisk.me/convertor/240x101/WDpTR7")
        if res:
            Db.collection.update_one({'_id': user_id}, {"$set": {'api': new_api}})
            msg = '✔ API ADDED: api update sucessful'
            print (msg)
            return msg
        else:
            msg = '❌ Wrong API'
            print(msg)
            return msg

    @classmethod
    def update_channel_link(cls, user_id, channel_link):
        Db.collection.update_one({'_id': user_id}, {"$set": {'channel_link': channel_link}})
        print('✔ Channel Link ADDED: Channel link update sucessful')



    # update Data on Mongo Db
    @classmethod
    def update_data_on_mongo_db(cls, user_id, new_data):
        Db.collection.update_one({'_id': user_id}, {"$set": new_data})
        print('update sucessfully')


    @classmethod
    def check_api_valid(cls, api, l):
            url = "https://diskuploader.mypowerdisk.com/v1/tp/cp"
            param = data = {"token": api, "link": f"{l}"}
            resp = requests.post(url, json=param)
            return str(resp) == '<Response [200]>'