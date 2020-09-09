from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

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
def index(): 
    cars = Car.query.all()
    return render_template("cars/index.html", cars=cars)
    

@mod.route('/search', methods=['GET', 'POST'])
#TODO: implement https://sqlalchemy-searchable.readthedocs.io/en/latest/integrations.html or https://pythonhosted.org/Flask-WhooshAlchemy/
def search_cars():
    form = searchForm(request.form)
    car = Car.query.search(form.keyWord).all()
    if car:
        return render_template("cars/details.html", car=car)
    return render_template("404.html")

