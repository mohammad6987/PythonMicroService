from flask import Flask, request, jsonify
from db import init_db
from user import User

app = Flask(__name__)
users_collection =init_db()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    existing_user = users_collection.find_one({"email": data['email']})
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400


    user = User(
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
    user_doc['_id'] = str(user_doc['_id'])  # ObjectId to string
    return jsonify(user_doc)

if __name__ == '__main__':
    app.run(port=5001)
