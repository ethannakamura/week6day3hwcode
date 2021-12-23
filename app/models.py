from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from uuid import uuid4

db = SQLAlchemy()

login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=True, default='')
    last_name = db.Column(db.String(100), nullable=True, default='')
    password = db.Column(db.String(150), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password) 
        self.id = str(uuid4())

class Player(db.Model):
    id = db.Column(db.String, primary_key=True)
    number = db.Column(db.Integer)
    first_name = db.Column(db.String(150), nullable=False) 
    last_name = db.Column(db.String(150), nullable=True) 
    position = db.Column(db.String(15))
    team = db.Column(db.String(150), nullable=False, default='Free Transfer')
    nationality = db.Column(db.String(150))
    transfer_cost = db.Column(db.String(150), nullable=False, default='$0m')

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'postion': self.position,
            'team': self.team,
            'nationality': self.nationality,
            'transfer_cost': self.transfer_cost
            }