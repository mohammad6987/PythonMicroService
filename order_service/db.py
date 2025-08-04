from pymongo import MongoClient,errors
def init_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["order_db"]
    orders_collection = db["orders"]


    return orders_collection
