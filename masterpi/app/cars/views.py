"""
.. module:: carsView
   :synopsis: List of API for cars function

"""
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import (
    current_user,
    login_required,
)

from app import db
from app.cars.models import Car, CarReport, CarLocation
from app.cars.maps import StaticMap
from flask_googlemaps import  Map, icons


mod = Blueprint('cars', __name__, url_prefix='/cars')


@mod.route('/details/<id>', methods=['GET'])
def details(id):
    """ 
    **Get detail information about the car**

    :param id: id of the car
    :type id: int

    :status 200: success
    :status 404: failed
    """
    car = Car.query.filter_by(id=id).first()
    if car.locations:
        gmap = StaticMap(car.current_location, id)
        carMap = gmap.create_map()
    else:
        carMap = None
    if car:
        return render_template("cars/details.html", car=car, carMap=carMap)
    return render_template("404.html")


@mod.route('/', methods=['GET'])
@login_required
def index():
    """
    **Get list of available car**

    This function allow user to get list of cars and its detail information

    :status 200: success
    :status 404: failed
    """
    cars = Car.query.all()
    return render_template("cars/index.html", cars=cars)
    



