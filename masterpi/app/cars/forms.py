from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, IntegerField
from wtforms.validators import Required, EqualTo, Email

class CarForm(Form):
    make = TextField('Make')
    body_type = TextField('Body Type')
    color = TextField('Color')
    seats = IntegerField('Seats')
    cost_per_hour = IntegerField('Cost Per Hour')
