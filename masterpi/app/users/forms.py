from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, SelectField
from wtforms.validators import Required, EqualTo, Email
from app.users import constants as USER

class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('Remember me')

class RegisterForm(Form):
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
        ])
    accept_tos = BooleanField('I accept the TOS', [Required()])

class UserForm(Form):
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    role = SelectField('Role', choices=[(0, USER.ROLE[0]), 
                                       (1, USER.ROLE[1]), 
                                       (2, USER.ROLE[2]),
                                       (3, USER.ROLE[3])])
    first_name = TextField('First Name')
    last_name = TextField('Last Name')

class UserEditForm(Form):
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Required(), Email()])
    role = SelectField('Role', choices=[(0, USER.ROLE[0]), 
                                       (1, USER.ROLE[1]), 
                                       (2, USER.ROLE[2]),
                                       (3, USER.ROLE[3])])
    first_name = TextField('First Name')
    last_name = TextField('Last Name')