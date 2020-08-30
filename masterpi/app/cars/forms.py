from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, IntegerField
from wtforms.validators import Required, EqualTo, Email

class searchForm(Form):
    keyWord = TextField('keyword', [Required()])

class CarForm(Form):
    make = TextField('Make')
    body_type = TextField('Body Type')
    color = TextField('Color')
    seats = IntegerField('Seats')
    cost_per_hour = IntegerField('Cost Per Hour')
