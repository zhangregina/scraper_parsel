import certifi
from pymongo import MongoClient
from decouple import config


class Mongo_DB:
    def __init__(self):
        self.connection_string = config("MONGO_DB_URL")
        self.client = MongoClient(self.connection_string, tlsCAFile=certifi.where())
        self.db = self.client["auto_mongo_db"]
        self.collection = self.db[
            "auto_collection"
        ]  # коллекция как таблица в реляционной бд

    def add_to_collection(self, auto_objects):
        self.collection.insert_one(auto_objects)
