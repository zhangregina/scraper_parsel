from datetime import datetime
import certifi
from pymongo import MongoClient
from decouple import config

#объединить две модельки в один большой словарь ?
class Mongo_DB:

    log_collection = {
        "_id": "",
        "vin_code": "",
        "url": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }

    auto_collection = {
        "_id": "",
        "current_url": "",
        "title": "",
        "price": "",
        "price_usd_euro": "",
        "actual_cost_date": "",
        "in_stock": "",
        "car_rating": "",
        "credit": "",
        "autosalon_name": "",
        "autosalon_rating": "",
        "location": "",
        "engine": "",
        "gearbox": "",
        "privod": "",
        "generation": "",
        "car_color": "",
        "available_color": "",
        "image": "",
        "max_speed": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }

    def __init__(self):
        self.connection_string = config("MONGO_DB_URL")
        self.client = MongoClient(self.connection_string, tlsCAFile=certifi.where())
        self.db = self.client["auto_mongo_db"]
        self.collection = self.db["log_collection"]  # коллекция как таблица в реляционной бд
        self.main_collection = self.db["auto_collection"]

    def add_to_log_collection(self, log_objects):
        self.collection.insert_one(log_objects)

    def add_to_auto_collection(self, auto_objects):
        self.main_collection.insert_one(auto_objects)
