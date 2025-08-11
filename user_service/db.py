from pymongo import MongoClient,errors
import os
def init_db():
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri)
    db = client["user_db"]
    users_collection = db["users"]

    try:
        users_collection.create_index("username", unique=True)
    except errors.OperationFailure as e:
        print("Index already exists or failed:", e)


    return users_collection
