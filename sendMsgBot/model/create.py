from pymongo import MongoClient

def get_database():
   client = MongoClient()

   db = client.parseAvito
   collection = db.Users

   return collection