from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import current_user

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport

mod = Blueprint('bookings', __name__, url_prefix = '/bookings')

@mod.route('/book', methods = ['POST'])
def book():
    car = Car.query.filter_by(id = request.form['car_id']).first()
    if car:
        user_id = current_user.id
    booking = Booking(user_id, car.id, request.form['duration'])
    db.session.add(booking)
    db.session.commit()
    bookingAction = BookingAction(booking.id, "created")
    db.session.add(bookingAction)
    db.session.commit()
    return '', 200

@mod.route('/unlock', methods = ['POST'])
def unlock():
    bookingAction = BookingAction(request.form['booking_id'], "unlocked")
    db.session.add(bookingAction)
    db.session.commit()
    return '', 200

@mod.route('/cancel', methods = ['POST'])
def cancel():
    bookingAction = BookingAction(request.form['booking_id'], "cancelled")
    db.session.add(bookingAction)
    db.session.commit()
    return '', 200

@mod.route('/return', methods = ['POST'])
def return_():
    bookingAction = BookingAction(request.form['booking_id'], "returned")
    db.session.add(bookingAction)
    booking = Booking.query.get(request.form['booking_id'])
    carLocation = CarLocation(booking.car_id, "Ho Chi Minh City")
    db.session.add(carLocation)
    db.session.commit()
    return '', 200
