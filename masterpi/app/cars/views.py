from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import (
    current_user,
    login_required,
)

from app import db
from app.cars.models import Car, CarReport
from app.cars.forms import searchForm


mod = Blueprint('cars', __name__, url_prefix='/cars')


@mod.route('/details/<id>', methods=['GET'])
def details(id):
    car = Car.query.filter_by(id=id).first()
    if car:
        return render_template("cars/details.html", car=car)
    return render_template("404.html")


@mod.route('/', methods=['GET'])
@login_required
def index(): 
    cars = Car.query.all()
    return render_template("cars/index.html", cars=cars)
    



