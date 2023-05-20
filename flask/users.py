from datetime import time

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, abort

from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


class UserRegister(Resource):

    def post(self):

        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        if username is None:
            return abort(400, message='Username not provided.')

        if password is None:
            return abort(400, message='Password not provided.')

        user = db.session.query(User).get(username)

        if user:
            return abort(401, message='Username already exists.')

        hashed_pw = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_pw,
            email=email,
        )
        db.session.add(user)


        db.session.commit()

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        response = jsonify({'message' : 'You have successfully registered.',
                            'access_token' : access_token,
                            'refresh_token' : refresh_token,
                            'username' : username,
                            })
        response.status_code=201

        return response

class UserLogin(Resource):

    def post(self):

        username = request.json['username']
        password = request.json['password']

        if username is None:
            return abort(400, message='Username not provided.')

        if password is None:
            return abort(400, message='Password not provided.')

        user = db.session.query(User).get(username)

        if not user:
            return abort(401, message='Username provided does not exist.')

        if not check_password_hash(user.password, password):
            return abort(401, message='Wrong Password')

        db.session.commit()

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)


        response = jsonify({'message' : 'You have been logged in successfully!',
                            'access_token' : access_token,
                            'refresh_token' : refresh_token,
                            'username': username,
                            })
        response.status_code=200

        return response