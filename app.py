from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models
import os
#import the blueprint
from api.user import user
from api.beer import beer


DEBUG = True
PORT = 8000

login_manager = LoginManager() # sets up ability to se up login

app = Flask(__name__, static_url_path="", static_folder="static")
# this is initializing an instance of the Flask class.
app.secret_key = "RAN@#$%^&*DOM STRING"
login_manager.init_app(app) #this sets up session on the app

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


CORS(user, origins=['http://localhost:3000', "https://beer-on-tap.herokuapp.com"], supports_credentials=True)
CORS(beer, origins=['http://localhost:3000', "https://beer-on-tap.herokuapp.com"], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(beer)

@app.before_request
def before_request():
    """ Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """ Close database after each request """
    return response

@app.route('/')
def index():
    return 'hi'


if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    # models.initialize()
    app.run(debug=DEBUG, port=PORT)