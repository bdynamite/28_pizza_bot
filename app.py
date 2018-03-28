from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_PATH')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BASIC_AUTH_USERNAME'] = getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = getenv('BASIC_AUTH_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True
app.secret_key = 'vfregv33f3'
basic_auth = BasicAuth(app)
admin = Admin(app)
db = SQLAlchemy(app)

