from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport
from app.bookings.forms import durationForm


mod = Blueprint('bookings', __name__, url_prefix='/bookings')

mod.route('/book-car/<id>', methods=['GET'])
def book_car(id):
    duration = durationForm(request.form)
    car = Car.query.filter_by(id=id).first()
    if car:
        user_id = session['user_id'] #not sure 
        booking = Booking(user_id, id, duration)
        bookingAction = BookingAction(booking.id, "book")
        db.session.add(bookingAction)
        db.session.add(booking)
        db.session.commit()
    return render_template("404.html")


mod.route('/cancel-booking/<booking_id>', methods=['GET'])
def cancel_booking(booking_id):
    bookingAction = BookingAction(booking_id, "cancel")
    db.session.add(bookingAction)
    db.session.commit()
    return render_template("404.html")