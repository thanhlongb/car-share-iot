from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.bookings.models import Booking, BookingAction

mod = Blueprint('bookings', __name__, url_prefix='/bookings')

