from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
with app.app_context():
    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.site.views import mod as siteModule
from app.users.views import mod as usersModule
from app.users.views import api_mod as usersAPIModule
from app.cars.views import mod as carsModule
from app.bookings.views import mod as bookingsModule
app.register_blueprint(siteModule)
app.register_blueprint(usersModule)
app.register_blueprint(usersAPIModule)
app.register_blueprint(carsModule)
app.register_blueprint(bookingsModule)
