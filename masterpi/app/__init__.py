from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from oauthlib.oauth2 import WebApplicationClient
from flask_googlemaps import GoogleMaps, Map, icons

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
mail.init_app(app)
GoogleMaps(app, key=app.config['GOOGLE_MAP_API_KEY'])

with app.app_context():
    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_found(error):
    return render_template('403.html'), 403

from app.users.views import mod as usersModule
from app.users.views import api_mod as usersAPIModule
from app.cars.views import mod as carsModule
from app.bookings.views import mod as bookingsModule
app.register_blueprint(usersModule)
app.register_blueprint(usersAPIModule)
app.register_blueprint(carsModule)
app.register_blueprint(bookingsModule)

#api
from app.users.api import api_mod as usersAPI
from app.cars.api import api_mod as carsAPI
from app.bookings.api import api_mod as bookingsAPI
app.register_blueprint(usersAPI)
app.register_blueprint(carsAPI)
app.register_blueprint(bookingsAPI)
