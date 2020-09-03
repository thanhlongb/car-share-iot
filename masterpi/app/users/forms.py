from flask_wtf import Form, RecaptchaField, FlaskForm
from wtforms import TextField, PasswordField, BooleanField, MultipleFileField, SubmitField
from wtforms.validators import Required, EqualTo, Email
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField

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

class PhotosForm(FlaskForm):
    images = FileField('Images', render_kw={'multiple':True},
    validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'jpg, png files only!')
    ])
