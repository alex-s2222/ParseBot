from pymongo import MongoClient
import os

def get_database():
   mongo_url = create_mongo_url_from_env()
   client = MongoClient(mongo_url)

   db = client.parseAvito
   collection = db.Users

   return collection


def create_mongo_url_from_env():
   """создаем ссылку на базу данных"""
   mongo_host = os.environ['MONGO_HOST']
   mongo_user = os.environ['MONGO_USER']
   mongo_password = os.environ['MONGO_PASSWORD']
   mongo_port = os.environ['MONGO_PORT']

   return 'mongodb://' + mongo_user + ':' + mongo_password +\
            '@' + mongo_host + ':' + mongo_port