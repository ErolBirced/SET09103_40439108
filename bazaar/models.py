from enum import unique
from flask.sessions import NullSession
from bazaar import db, login_manager, bcrypt
from flask_login import UserMixin

# Necessary to avoid exception error.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Here is the table for the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=60), nullable =False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

@property
def password(self):
    return self.password

@password.setter
def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=2000), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

# This is known as dunder dpr, and to be honest I do not fully understand it myself
# Did not work properly, was meant to overwrite the database names like "Item1" and "Item2"
# UPDATE: It works now, I do not know why.
    def __repr__(self):
        return f'Item {self.name}'
