from mongoengine import Document, StringField, FloatField, IntField

class Order(Document):
    user_id = StringField(required=True)
    product_name = StringField(required=True)
    price = FloatField(required=True)
    quantity = IntField(required=True)
