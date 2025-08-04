from flask import Flask, request, jsonify
from db import init_db
from models import User
from queue import publish_user_created

app = Flask(__name__)
init_db()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    ).save()
    publish_user_created(user.to_mongo().to_dict())
    return jsonify(user.to_mongo()), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_mongo())

if __name__ == '__main__':
    app.run(port=5001)
