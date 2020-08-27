from app import db
from sqlalchemy.inspection import inspect
from app.users import constants as USER

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.SmallInteger, default=USER.CUSTOMER)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    facial_recognition = db.Column(db.Boolean, default=False)
    google_login = db.Column(db.Boolean, default=False)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def getRole(self):
        return USER.ROLE[self.role]

    def serialize(self):
        data = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del data['password']
        return data

    def __repr__(self):
        return '<User %r>' % (self.username)