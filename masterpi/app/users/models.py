from app import db
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from app.users import constants as USER
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.SmallInteger, default=USER.CUSTOMER)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bluetooth_MAC = db.Column(db.String(100), nullable=True)
    facial_recognition = db.Column(db.Boolean, default=False)
    google_login = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, email, username=None, password=None,
                       role=None, first_name=None, last_name=None, 
                       bluetooth_MAC=None):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.bluetooth_MAC = bluetooth_MAC

    def isAdmin(self):
        return self.role == 0

    def isManager(self):
        return self.role == 1

    def isEngineer(self):
        return self.role == 2 

    def isCustomer(self):
        return self.role == 3

    def getRole(self):
        return USER.ROLE[self.role]

    def serialize(self):
        data = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del data['password']
        return data

    def serialize_with_cols(self, cols):
        data = {}
        for c in cols:
            if c == 'date':
                data[c] = getattr(self, c).strftime("%Y-%m-%d")
            else: 
                data[c] = getattr(self, c)
        return data

    def __repr__(self):
        return '<User %r>' % (self.email)
