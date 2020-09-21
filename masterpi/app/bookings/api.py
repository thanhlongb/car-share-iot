from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_login import current_user

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport
from app.calendar_api.calendar_api import CalendarApi
from app.users.models import User

from datetime import datetime

api_mod = Blueprint('booking', __name__, url_prefix='/api')

@api_mod.route('/bookings/book', methods = ['POST'])
def book():
    car = Car.query.filter_by(id = request.form['car_id']).first()
    if car:
        user_id = request.form['user_id']
    booking = Booking(user_id, car.id, request.form['duration'])
    db.session.add(booking)
    db.session.commit()
    bookingAction = BookingAction(booking.id, "created")
    db.session.add(bookingAction)
    db.session.commit()
    add_event_for_calendar(booking, bookingAction)
    return 'success', 200

@api_mod.route('/bookings/unlock', methods = ['POST'])
def unlock():
    """ API for unlocking (POST) a car

        a booking action record is created

        :<json int booking_id: id of a booking record

        :status 200: book created
    """
    bookingAction = BookingAction(request.form['booking_id'], "unlocked")
    db.session.add(bookingAction)
    db.session.commit()
    return 'success', 200

@api_mod.route('/bookings/cancel', methods = ['POST'])
def cancel():
    """ API for cancelling (POST) a booking
        
        a booking action record is created

        :<json int booking_id: id of a booking record

        :status 200: book canceled
    """
    bookingAction = BookingAction(request.form['booking_id'], "cancelled")
    db.session.add(bookingAction)
    db.session.commit()
    return 'success', 200

@api_mod.route('bookings/return', methods = ['POST'])
def return_():
    """ API for user to return (POST) a car

        a booking action record is created

        :<json int booking_id: id of a booking record

        :status 200: return succeed 
    """
    bookingAction = BookingAction(request.form['booking_id'], "returned")
    db.session.add(bookingAction)
    booking = Booking.query.get(request.form['booking_id'])
    carLocation = CarLocation(booking.car_id, "Ho Chi Minh City")
    db.session.add(carLocation)
    db.session.commit()
    return 'success', 200

def add_event_for_calendar(booking, bookingAction):
    """ This function will sent a calendar event to user who book the car 

    :param booking: booking of the car
    :param bookingAction: the booking action record of the car

    """
    user = User.query.filter_by(id = booking.user_id).first()
    title = "Book car {}".format(booking.car_id)
    description = "You have booked car {} at {} for {} hours. Your booking id is {}".format(booking.car_id, 
                                                                                            bookingAction.creation_time, 
                                                                                            booking.duration, 
                                                                                            booking.id)
    event = CalendarApi(title, description, user.email, bookingAction.creation_time, booking.duration)