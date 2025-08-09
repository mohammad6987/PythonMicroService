from flask import Flask, request, jsonify
from db import init_db
from models import User
from kafka_queue import init_queue,init_consumer
from threading import Thread
import json
app = Flask(__name__)
users_collection =init_db()
kafka_queue = init_queue()
kafka_consumer =init_consumer()
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    existing_user = users_collection.find_one({"username": data['username']})
    if existing_user:
        return jsonify({"error": "Username already registered"}), 400


    user = User(
        username =data['username'],
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    result = users_collection.insert_one(user.to_dict())
    user_doc = users_collection.find_one({"_id": result.inserted_id})
    user_doc['_id'] = str(user_doc['_id'])  
    return jsonify(user_doc), 201



@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    from bson import ObjectId
    user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        return jsonify({'error': 'User not found'}), 404
    user_doc['_id'] = str(user_doc['_id'])  
    return jsonify(user_doc)


def get_messages_from_services():
    for message in kafka_consumer:
        if not message.value:
            continue  
        try:
            print("Received:", message.value)
            msg_value = message.value  
            if msg_value and msg_value.get("header") == "get_username_for_orders":
                get_username_and_return_info(msg_value)
        except json.JSONDecodeError as e:
            print("Invalid JSON message:", message.value, e)



def get_username_and_return_info(msg):
    username = msg.get("username")
    reply_topic = msg.get("reply_topic")
    correlation_id = msg.get("correlation_id")
    
    if not username or not reply_topic:
        print("Invalid message: missing username or reply_topic")
        return

    user_doc = users_collection.find_one({"username": username})
    
    response = {
        "correlation_id": correlation_id,
        "header": "user_info_response"
    }
    
    if user_doc:
        response.update({
            "status": "success",
            "user_info": {
                "id": str(user_doc['_id']),
                "username": user_doc['username'],
                "name": user_doc['name'],
                "email": user_doc['email'],
                "phone": user_doc['phone']
            }
        })
    else:
        response.update({
            "status": "error",
            "message": f"User {username} not found"
        })
    
    kafka_queue.send(reply_topic, value=response)



if __name__ == '__main__':
    Thread(target= get_messages_from_services , daemon= True).start()
    
    app.run(port=5001)
