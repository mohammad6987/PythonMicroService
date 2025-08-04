from mongoengine import connect

def init_db():
    connect(
        db="user_db",
        host="localhost",
        port=27017
    )
