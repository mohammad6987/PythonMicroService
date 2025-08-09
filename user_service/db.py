from pymongo import MongoClient,errors
def init_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["user_db"]
    users_collection = db["users"]

    try:
        users_collection.create_index("username", unique=True)
    except errors.OperationFailure as e:
        print("Index already exists or failed:", e)


    return users_collection
