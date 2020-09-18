from app import db
from sqlalchemy.inspection import inspect
from app.users import constants as USER
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Declare user table and its attributes
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.SmallInteger, default=USER.CUSTOMER)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bluetooth_MAC = db.Column(db.String(100), unique=True, nullable=True)
    facial_recognition = db.Column(db.Boolean, default=False)
    google_login = db.Column(db.Boolean, default=False)

    def __init__(self, email, username=None, password=None,
                       role=None, first_name=None, last_name=None):
        """Create a an record of an user
            
        :param str email: The user email
        :param str username: Name for login
        :param str password: The password of the user
        :param int role: The role of the user from 0 - 3. 0: admin, 1: 
        :param str first_name: user first name
        :param str last_name: user last name
        """
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.bluetooth_MAC = bluetooth_MAC

    def isAdmin(self):
        """set the user role to admin

        :return: set the role attribute of user to 0
        """
        return self.role == 0

    def isManager(self):
        """set the user role to Manager

        :return: set the role attribute of user to 1
        """
        return self.role == 1

    def isEngineer(self):
        """set the user role to Engineer

        :return: set the role attribute of user to 2
        """
        return self.role == 2 

    def isCustomer(self):
        """set the user role to Customer

        :return: set the role attribute of user to 3
        """
        return self.role == 3

    def getRole(self):
        """get the user role

        :return: Role of user
        """
        return USER.ROLE[self.role]

    def serialize(self):
        """Convert user information to JSON format

        :return: data of user (exclude password) in JSON
        """
        data = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del data['password']
        return data

    def __repr__(self):
        return '<User %r>' % (self.email)