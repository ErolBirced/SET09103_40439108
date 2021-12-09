from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app = Flask(__name__)
# Creating database through SQLite, SQLAlchemy
# Storing passwords with hash through flask bcrypt(ATTEMPTED)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bazaar.db'
app.config['SECRET_KEY'] = '6163cef73fd49e261539ebdf'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from bazaar import routes
