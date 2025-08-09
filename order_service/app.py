from flask import Flask, request, jsonify
from db import init_db
from models import Order
from kafka import KafkaProducer, KafkaConsumer
from threading import Thread
import uuid
import json
import time
from bson import ObjectId

app = Flask(__name__)
order_collection = init_db()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

user_responses = {}
response_lock = Thread.Lock()


def start_consumer():
    consumer = KafkaConsumer(
        'order_service_replies',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    
    for message in consumer:
        msg_value = message.value
        if msg_value and 'correlation_id' in msg_value:
            with response_lock:
                correlation_id = msg_value['correlation_id']
                user_responses[correlation_id] = msg_value

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        username=data['username'],  
        product_name=data['product_name'],
        price=data['price'],
        quantity=data['quantity']
    )
    result = order_collection.insert_one(order.to_dict())
    

    order_doc = order_collection.find_one({"_id": result.inserted_id})
    order_doc['_id'] = str(order_doc['_id'])
    return jsonify(order_doc), 201

@app.route('/orders/user/<username>', methods=['GET'])
def get_orders(username):

    orders = list(order_collection.find({"username": username}))
    for order in orders:
        order['_id'] = str(order['_id'])
    

    correlation_id = str(uuid.uuid4())
    request_msg = {
        "header": "get_username_for_orders",
        "username": username,
        "reply_topic": "order_service_replies",
        "correlation_id": correlation_id
    }
    
    with response_lock:
        user_responses[correlation_id] = None 
    
    producer.send('user_requests', value=request_msg)
    
    user_info = None
    timeout = 5 
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        with response_lock:
            response = user_responses.get(correlation_id)
            if response and response.get('header') == 'user_info_response':
                if response.get('status') == 'success':
                    user_info = response.get('user_info')
                
                del user_responses[correlation_id]
                break
        time.sleep(0.1)  
    
    if not user_info:
        user_info = {"error": "User service timeout"}
    
    return jsonify({
        "user_info": user_info,
        "orders": orders
    })

if __name__ == '__main__':
    Thread(target=start_consumer, daemon=True).start()
    app.run(port=5002)