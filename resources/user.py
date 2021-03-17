import hashlib
import werkzeug
import os

from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, 
    jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required, 
    jwt_required, get_raw_jwt)
from blacklist import BLACKLIST

from models.user import UserModel


class User(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)
        
        if user:
            return user.json()
        
        return {
            "message": "User not found!"
        }, 404
    
    @fresh_jwt_required
    def delete(self, id):
        user = UserModel.find_by_id(id)
        
        if user:
            user.remove_from_db()
            return {"message": "User deleted!"}, 200

        return {
            "message": "User not found!"
        }, 404


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'fullname', 
        type=str, 
        default='',
        required=False)
    parser.add_argument(
        'username', 
        type=str, 
        required=True,
        help='This field cannot be blank.')
    parser.add_argument(
        'phone', 
        type=str, 
        required=False)
    parser.add_argument(
        'address', 
        type=str, 
        required=False)
    parser.add_argument(
        'email', 
        type=str, 
        required=True, 
        help='This field cannot be blank.')
    parser.add_argument(
        'password', 
        type=str, 
        required=True, 
        help='This field cannot be blank.')
    parser.add_argument(
        'organization', 
        type=str, 
        default='',
        required=False)
    parser.add_argument(
        'position', 
        type=str, 
        default='',
        required=False)
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists!"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists!"}, 400

        if UserModel.find_by_phone(data['phone']):
            return {"message": "A user with that phone already exists!"}, 400

        data['password'] = hashlib.sha256(data["password"]\
            .encode("utf-8")).hexdigest()
        data['date_created'] = datetime.utcnow()
        data['date_modified'] = datetime.utcnow()
        data['avatar'] = 'default_avatar.png'
        data['status'] = 0

        user = UserModel(
            data['fullname'],
            data['username'],
            data['phone'],
            data['address'],
            data['email'],
            data['password'],
            data['date_created'],
            data['date_modified'],
            data['avatar'],
            data['status'],
            data['organization'],
            data['position']
        )
        
        user.save_to_db()

        return {
            "message": f"User with username {data['username']} created successfully."
        }, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', 
        type=str, 
        required=True,
        help='This field cannot be blank.')
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be blank.')
    
    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and user.password == hashlib.sha256(data["password"]\
            .encode("utf-8")).hexdigest():
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {
            "message": "Invalid credentials!"
        }, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class UserUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'fullname', 
        type=str, 
        required=False)
    parser.add_argument(
        'username', 
        type=str, 
        required=False)
    parser.add_argument(
        'phone', 
        type=str, 
        required=False)
    parser.add_argument(
        'address', 
        type=str, 
        required=False)
    parser.add_argument(
        'email', 
        type=str, 
        required=False)
    parser.add_argument(
        'password', 
        type=str, 
        required=False)
    parser.add_argument(
        'status', 
        type=str, 
        required=False)
    parser.add_argument(
        'organization', 
        type=str, 
        required=False)
    parser.add_argument(
        'position', 
        type=str, 
        required=False)
    
    @fresh_jwt_required
    def put(self, id):
        data = UserUpdate.parser.parse_args()

        user = UserModel.find_by_id(id)

        if not user:
            return {
                "message": "User not found!"
            }, 404
        
        if data['fullname'] is not None:
            user.fullname = data['fullname']
        if data['username'] is not None:
            user.username = data['username']
        if data['phone'] is not None:
            user.phone = data['phone']
        if data['address'] is not None:
            user.address = data['address']
        if data['email'] is not None:
            user.email = data['email']
        if data['password'] is not None:
            user.password = hashlib.sha256(data["password"]\
                .encode("utf-8")).hexdigest()
        if data['status'] is not None:
            user.status = data['status']            
        if data['organization'] is not None:
            user.organization = data['organization']
        if data['position'] is not None:
            user.position = data['position']

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred updating the user."}, 500
        
        return {
            "message": f"User with id {id} updated successfully."
        }, 201


class AvatarUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'avatar',
        type=werkzeug.datastructures.FileStorage,
        required=True,
        location='files',
        help='This field cannot be blank.')

    def put(self, username):
        data = AvatarUpload.parser.parse_args()

        user = UserModel.find_by_id(id)

        if not user:
            return {
                "message": "User not found!"
            }, 404
        
        try:
            filename = str(user.username + '.jpg')
            data['avatar'].save(os.path.join('static/avatar', filename))

            user.avatar = filename
            user.save_to_db()
            
            return {
                "message": f"User with username {username} updated successfully."
            }, 201
        except:
            return {"message": "An error occurred updating the avatar."}, 500


class UserList(Resource):
    @jwt_required
    def get(self):
        return [x.json() for x in UserModel.query.all()]


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {
            "access_token": new_token
        }, 200
