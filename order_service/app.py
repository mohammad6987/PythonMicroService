from flask import Flask, request, jsonify
from db import init_db
from models import Order
from kafka_consumer import start_consumer

app = Flask(__name__)
order_collection = init_db()

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        user_id=data['user_id'],
        product_name=data['product_name'],
        price=data['price'],
        quantity=data['quantity']
    )
    res = order_collection.insert_one(order.to_dict())

@app.route('/orders/user/<user_id>', methods=['GET'])
def get_orders(user_id):
    orders = order_collection.find
    return jsonify([o.to_mongo() for o in orders])

if __name__ == '__main__':
    start_consumer()
    app.run(port=5002)
from flask import Flask, request, jsonify
from db import orders_collection
import requests
from bson import ObjectId

app = Flask(__name__)