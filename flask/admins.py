from flask_restful import Resource, abort
from flask import request, jsonify, json
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from models import Admin, db
from werkzeug.security import check_password_hash,generate_password_hash

class AdminLogin (Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']

        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            return abort(401, message="Username is incorrect")

        pass_match = check_password_hash(admin.password, password)
        if not pass_match:
            return abort(401, message="Password incorrect")
        else:
            accessToken=create_access_token(identity=username)
            refresh_token=create_refresh_token(identity=username)

            response= jsonify({
                'message' : 'Admin logged in successfully!',
                "accessToken":accessToken,
                "refresh_token":refresh_token,
                "username":username,
            })
            response.status_code=200
            return response

