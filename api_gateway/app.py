from flask import Flask, request, jsonify
import requests
import os
import json
from threading import Thread
from kafka import KafkaConsumer

app = Flask(__name__)

# Service URLs
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5002')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')



def forward_request(service_url, path):
    url = f"{service_url}{path}"
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        params=request.args,
        allow_redirects=False
    )
    
    try:
        return jsonify(response.json()), response.status_code
    except:
        return response.content, response.status_code




@app.route('/orders', methods=['POST'])
def create_order():
    return forward_request(ORDER_SERVICE_URL, '/orders')

@app.route('/orders/user/<username>', methods=['GET'])
def get_user_orders(username):
    return forward_request(ORDER_SERVICE_URL, f'/orders/user/{username}')




@app.route('/users', methods=['POST'])
def create_user():
    return forward_request(USER_SERVICE_URL, '/users')

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return forward_request(USER_SERVICE_URL, f'/users/{user_id}')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)