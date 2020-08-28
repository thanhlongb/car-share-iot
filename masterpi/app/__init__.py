from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

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
