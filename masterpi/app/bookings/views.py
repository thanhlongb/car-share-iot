from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport

mod = Blueprint('bookings', __name__, url_prefix='/bookings')

@mod.route('/book-car', methods=['POST'])
def book_car():
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        user_id = session['user_id'] 
        booking = Booking(user_id, car.id, request.form['duration'])
        db.session.add(booking)
        db.session.commit()
        bookingAction = BookingAction(booking.id, "book")
        db.session.add(bookingAction)
        db.session.commit()
    return render_template("404.html")


@mod.route('/cancel-booking', methods=['POST'])
def cancel_booking(booking_id):
    bookingAction = BookingAction(booking_id, "cancel")
    db.session.add(bookingAction)
    db.session.commit()
    return render_template("404.html")