from pymongo import MongoClient,errors
import os
def init_db():
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client["order_db"]
    orders_collection = db["orders"]


    return orders_collection
