from mongoengine import connect

def init_db():
    connect(
        db="order_db",
        host="localhost",
        port=27017
    )
