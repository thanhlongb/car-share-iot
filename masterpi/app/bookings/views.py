from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport



mod = Blueprint('bookings', __name__, url_prefix='/bookings')


def book_car(car_id, duration):
    car = Car.query.filter_by(id=id).first()
    if car:
        user_id = session['user_id'] #not sure 
        booking = Booking(user_id, car_id, duration)

        db.session.add(booking)
        db.session.commit()
    return render_template("404.html")


def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=id).first()
    if booking:
        db.session.add(booking)
        db.session.commit()
    return render_template("404.html")