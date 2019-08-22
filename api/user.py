import models

import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

# fist arg. is the blueprint name,
# 2nd is the import name
# 3rd is what every route in the blueprint will start with
user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
    #this function has to deal with PILLOW
    # purpse is to save the image as a static asset.
    # 1. to generate a random name
    random_hex = secrets.token_hex(8)

    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext

    # create the file_path
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)

    #pillow code
    output_size = (125, 175)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path_for_avatar)

    return file_path_for_avatar 

# 'user' refers to the blueprint name
@user.route('/register', methods=["POST"])
def register(): 
    #this is who we grabe the image from the login
    pay_file = request.files
    # this has the form info from the dict.
    # we change the request object into a dict.
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()

    print(payload)
    print(dict_file)

    payload['username'].lower() # make username lowercase
    try:
        #check to see if email exists, if it does let user know. the .get() comes from peeweee
        models.User.get(models.User.username == payload['username']) # query to find user by their email. if this model is found, responde to client
        return jsonify(data={}, status={"code": 401, "message": "The user with this name exisits"})
    except models.DoesNotExist: #boolean on the model
        # if model doesnt exisit, we will create/reg this user
        # we need to hash the password, 
        payload['password'] = generate_password_hash(payload['password'])
        #function that will save the image as a static asset.
        file_picture_path = save_picture(dict_file['file'])
        # save_picture is a helper function that we will create above

        # this sets the image property to be the file_picture_path
        payload['image'] = file_picture_path

        ## create the row in the table 
        user = models.User.create(**payload)

        print(type(user)) # => class User user is an instance of 
        login_user(user) #login_user is from flask_login
        
        current_user.image = file_picture_path

        # we cant send back a class. we can only send back dists and lists. 
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        #remove the password
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
            print(user, '<-- this is the user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password was incorrect."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password was incorrect."})
























