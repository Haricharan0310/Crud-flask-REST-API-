import flask
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/crud"
mongo = PyMongo(app)
print(mongo.db)
print(mongo.db.users.find_one({"name":"John"}))
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    # user_data['password'] = generate_password_hash(user_data['password'])
    user_id = mongo.db.users.insert_one(user_data)
    return jsonify({'message': 'User created successfully', 'user_id': str(user_id)})

@app.route('/', methods=['GET'])
def get_users():
    users1 = mongo.db.users.find()
    return flask.jsonify([x for x in users1])
    # user_list = []
    # for user in users:
    #     user['_id'] = str(user['_id'])
    #     user_list.append(user)
    # return jsonify(user_list)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one_or_404({'_id': ObjectId(user_id)})
    user['_id'] = str(user['_id'])
    return jsonify(user)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    if 'password' in user_data:
        user_data['password'] = generate_password_hash(user_data['password'])
    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return jsonify({'message': 'User deleted successfully'})


if __name__ == "__main__":
    app.run(debug=True)