from flask import Flask, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
import os
app = Flask(__name__)
app.secret_key = 'thissecret'
login_manager = LoginManager()
login_manager.init_app(app)

import models
from resources.pins import pins
from resources.users import users
from resources.messages import messages

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data = {
            'error': 'User not logged in'
        },
        status = {
            'code': 401,
            'message': 'You must be logged'
        }
    )

CORS(pins, origins=['http://localhost:3000', 'https://pinpals-react.herokuapp.com/', 'http://pinpals-react.herokuapp.com/'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000', 'https://pinpals-react.herokuapp.com/', 'http://pinpals-react.herokuapp.com/'],
supports_credentials=True)
CORS(messages, origins=['http://localhost:3000', 'https://pinpals-react.herokuapp.com/', 'http://pinpals-react.herokuapp.com/'], supports_credentials=True)

app.register_blueprint(pins, url_prefix='/api/v1/pins')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(messages, url_prefix='/api/v1/messages')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'ON'

DEBUG = True
PORT = 8000
if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)