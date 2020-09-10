from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import TextField, PasswordField, BooleanField, SelectField, MultipleFileField, SubmitField, FileField
from wtforms.validators import Required, EqualTo, Email
from app.users import constants as USER
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])
    remember_me = BooleanField('Remember me')

class RegisterForm(Form):
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])
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
class PhotosForm(FlaskForm):
    images = FileField('Images', render_kw={'multiple':True},
    validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'jpg, png files only!')
    ])
