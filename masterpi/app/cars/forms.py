from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email

class searchForm(Form):
    keyWord = TextField('keyword', [Required()])
