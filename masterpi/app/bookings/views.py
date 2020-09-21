from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from flask_login import current_user

from app import db
from app.bookings.models import Booking, BookingAction
from app.cars.models import Car, CarLocation, CarReport
from app.cars.utils import get_current_location_coordinate, get_current_location_name
from app.calendar_api.calendar_api import CalendarApi
from app.users.models import User

from datetime import datetime


mod = Blueprint('bookings', __name__, url_prefix = '/bookings')

@mod.route('/book', methods = ['POST'])
def book():
    """ This function allow user to book (POST) a car

        When user book a car, a booking record and booking action is created 

        :<json int car_id: id of a existing car
        :<json int duration: book duration (hours)

        :status 200: book created
    """
    car = Car.query.filter_by(id = request.form['car_id']).first()
    if car:
        user_id = current_user.id
    booking = Booking(user_id, car.id, request.form['duration'])
    db.session.add(booking)
    db.session.commit()
    bookingAction = BookingAction(booking.id, "created")
    db.session.add(bookingAction)
    db.session.commit()
    add_event_for_calendar(booking, bookingAction)
    return '', 200

@mod.route('/unlock', methods = ['POST'])
def unlock():
    """ This function allow user to unlock (POST) a car

        a booking action record for unlock is created

        :<json int booking_id: id of a booking record

        :status 200: car unlocked
    """
    bookingAction = BookingAction(request.form['booking_id'], "unlocked")
    db.session.add(bookingAction)
    db.session.commit()
    return '', 200

@mod.route('/cancel', methods = ['POST'])
def cancel():
    """ This function allow user to cancel (POST) a booking
        
        a booking action record for cancel booking is created

        :<json int booking_id: id of a booking record

        :status 200: book canceled
    """
    bookingAction = BookingAction(request.form['booking_id'], "cancelled")
    db.session.add(bookingAction)
    db.session.commit()
    return '', 200

@mod.route('/return', methods = ['POST'])
def return_():
    """ This function allow user to return (POST) a car

        a booking action record is created

        :<json int booking_id: id of a booking record

        :status 200: return succeed 
    """
    bookingAction = BookingAction(request.form['booking_id'], "returned")
    db.session.add(bookingAction)
    booking = Booking.query.get(request.form['booking_id'])
    current_location_coordinate = get_current_location_coordinate()
    current_location_name = get_current_location_name(**current_location_coordinate)
    carLocation = CarLocation(booking.car_id,
                              long=current_location_coordinate['lng'],
                              lat=current_location_coordinate['lat'],
                              location=current_location_name)
    db.session.add(carLocation)
    db.session.commit()
    return '', 200

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