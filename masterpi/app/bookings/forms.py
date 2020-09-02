from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class durationForm(Form):
    duration = TextField('duration', [Required()])
