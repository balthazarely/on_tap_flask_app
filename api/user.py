import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user', url_prefix='/user') 

@user.route('/register', methods=["POST"])
def register(): 
    print('This is in my register route')

    payload = request.form.to_dict()
    print(payload)
    payload['username'].lower() 
    try:
        models.User.get(models.User.username == payload['username']) 
        return jsonify(data={}, status={"code": 401, "message": "The user with this name exisits"})
    except models.DoesNotExist: 

        payload['password'] = generate_password_hash(payload['password'])

        user = models.User.create(**payload)

        print(type(user))  
        login_user(user) 
        

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

# user login route, Whoop whoop!
@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '<-- this is the payload')
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password was incorrect."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password was incorrect."})

# Logout route to kill session
@user.route("/logout")

def logout():
    logout_user()
    print(user, "<-- this is logged out user")
    return jsonify(status={"code": 200, "message": "Success"})


# Show route
@user.route('/<id>', methods=["GET"])
def get_one_user(id):
    user = models.User.get_by_id(id)
    return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})

# Update route
@user.route('/<id>', methods=["PUT"])
def update_comments(id):
    payload = request.get_json()
    # payload_to_dict = payload.to_dict()
    print(payload, '<-- this is payload in edit route')
    query = models.User.update(**payload).where(models.User.id == id)
    query.execute()
    update_comments = models.User.get_by_id(id)
    print(update_comments, '<-- this is in the edit route... update_comments')
    return jsonify(data=model_to_dict(update_comments), status={"code": 200, "message": "Success"})
   

# Delete route
@user.route('/<id>', methods=["Delete"])
def delete_user_comments(id):
    query = models.User.delete().where(models.User.id == id)
    query.execute()
    return jsonify(data='comment was deleted', status={"code": 200, "message": "Successfully deleted comment"})














