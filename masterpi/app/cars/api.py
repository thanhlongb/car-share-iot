import os, pickle, json

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, and_, desc, func
from flask_mail import Message

from app import db, login_manager, client, mail
from app.cars.models import Car, CarReport
from app.cars.forms import CarForm
from app.users.models import User

api_mod = Blueprint('car', __name__, url_prefix='/api')

#----------------- cars API -----------------#
@api_mod.route('/cars/', methods=['GET'])
def get_cars():
    """ Get all car record 

    :returns: list of cars in JSON format
    """
    cars = Car.query.order_by(desc(Car.id)).all()
    data = [r.serialize() for r in cars]
    return jsonify(data)

@api_mod.route('/cars/create', methods=['POST'])
def cars_create():
    """ Create a car record

        :param string make: car brand
        :param string color: car color
        :param string body_type: car body type
        :param int seats: number of seats
        :param int cost_per_hour: cost per hour

        :returns: Car in JSON format
    """
    form = CarForm(request.form)
    car = Car(make=form.make.data, 
                color=form.color.data,
                body_type=form.body_type.data,
                seats=form.seats.data,
                cost_per_hour=form.cost_per_hour.data)
    db.session.add(car)
    db.session.commit()
    return car.serialize()

@api_mod.route('/cars/edit/<car_id>', methods=['POST'])
def cars_update(car_id):
    """ Update car record

        :param car_id: id of existing car
    """
    car = Car.query.filter_by(id=car_id).first()
    if not car: 
        return "400 car not exists"
    form = CarForm(obj=request.form)
    form.populate_obj(car)
    db.session.commit()
    return car.serialize()

@api_mod.route('/cars/delete', methods=['DELETE'])
def users_delete():
    """ Delete a car

    :param car_id: id of existing car
    """
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        return car.serialize(), 200
    return 'car not exist.', 404

#----------------- cars report API -----------------#
@api_mod.route('/cars/report', methods=['POST'])
def cars_report():
    """ Return all report of the car
    """
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        car_report = CarReport(car.id)
        db.session.add(car_report)
        db.session.commit()
        return 'success', 200
    return 'car not exist.', 404

@api_mod.route('/cars/reports/assign', methods=['POST'])
def reports_assign():
    """ Assign a task 
    """
    report = CarReport.query.filter_by(id=request.form['report_id']).first()
    if report:
        report.fixer_id = request.form['engineer_id']
        db.session.commit()
        fixer = User.query.filter_by(id=request.form['engineer_id']).first()
        email = Message("There is a new vehicle with issues reported!",
                        recipients=[fixer.email])
        mail.send(email)
        return 'success', 200
    return 'report not exist.', 404

@api_mod.route('/engineer/reports/fixed', methods=['POST'])
def reports_fixed():
    """ Update a report
    """
    report = CarReport.query.filter_by(id=request.form['report_id']).first()
    if report:
        report.fixed = True
        db.session.commit()
        return 'success', 200
    return 'report not exist.', 404