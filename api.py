from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['userdb']
collection = db['users']

class User(Resource):
    def get(self, user_id=None):
        if user_id:
            user = collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
                return user, 200
            else:
                return {'message': 'User not found'}, 404
        else:
            users = []
            for user in collection.find():
                user['_id'] = str(user['_id'])
                users.append(user)
            return users, 200

    def post(self):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        new_user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = collection.insert_one(new_user)
        new_user['_id'] = str(result.inserted_id)
        return new_user, 201

    def put(self, user_id):
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        updated_user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': updated_user})
        if result.modified_count == 0:
            return {'message': 'User not found'}, 404
        else:
            updated_user['_id'] = user_id
            return updated_user, 200

    def delete(self, user_id):
        result = collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 0:
            return {'message': 'User not found'}, 404
        else:
            return {'message': 'User deleted successfully'}, 200

api.add_resource(User, '/users', '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
