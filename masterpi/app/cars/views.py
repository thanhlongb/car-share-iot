from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.cars.models import Car, CarLocation, CarReport

mod = Blueprint('cars', __name__, url_prefix='/cars')
