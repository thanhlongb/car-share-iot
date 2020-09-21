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
    cars = Car.query.order_by(desc(Car.id)).all()
    data = [r.serialize() for r in cars]
    return jsonify(data)

@api_mod.route('/cars/create', methods=['POST'])
def cars_create():
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
    car = Car.query.filter_by(id=car_id).first()
    if not car: 
        return "400 car not exists"
    form = CarForm(obj=request.form)
    form.populate_obj(car)
    db.session.commit()
    return car.serialize()

@api_mod.route('/cars/delete', methods=['DELETE'])
def users_delete():
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        return car.serialize(), 200
    return 'car not exist.', 404

#----------------- cars report API -----------------#
@api_mod.route('/cars/report', methods=['POST'])
def cars_report():
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        car_report = CarReport(car.id)
        db.session.add(car_report)
        db.session.commit()
        return 'success', 200
    return 'car not exist.', 404

@api_mod.route('/cars/reports/assign', methods=['POST'])
def reports_assign():
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
    report = CarReport.query.filter_by(id=request.form['report_id']).first()
    if report:
        report.fixed = True
        db.session.commit()
        return 'success', 200
    return 'report not exist.', 404