from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

from app import db
from app.users.forms import RegisterForm, LoginForm, UserForm, UserEditForm
from app.users.models import User
from app.cars.models import Car, CarReport
from app.cars.forms import CarForm
from app.bookings.models import Booking
from app.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')
api_mod = Blueprint('users_api', __name__, url_prefix='/api/users')

@mod.route('/me/')
@requires_login
def home():
    return render_template("users/profile.html", user=g.user)

@mod.route('/logout/')
@requires_login
def logout():
    session['user_id'] = None
    return redirect(url_for('users.login'))
    
@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # we use werzeug to validate user's password
        if user and check_password_hash(user.password, form.password.data):
            # the session can't be modified as it's signed, 
            # it's a safe place to store the user id
            session['user_id'] = user.id
            flash('Welcome %s' % user.username)
            return redirect(url_for('users.home'))
        flash('Wrong username or password', 'error-message')
    return render_template("users/login.html", form=form)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # check whether if there is user with the same username/email
        user = User.query.filter(
            or_(
                User.username == form.username.data,
                User.email == form.email.data
            )
        ).first()
        if not user:
            # create an user instance not yet stored in the database
            user = User(username=form.username.data, email=form.email.data, \
                password=generate_password_hash(form.password.data))
            # Insert the record in our database and commit it
            db.session.add(user)
            db.session.commit()

            # Log the user in, as he now has an id
            session['user_id'] = user.id

            # flash will display a message to the user
            flash('Thanks for registering')
            # redirect user to the 'home' method of the user module.
            return redirect(url_for('users.home'))
        flash('Email address or username is taken.')
    return render_template("users/register.html", form=form)
    
@mod.route('/booking-history/', methods=['GET'])
@requires_login
def booking_history():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template("users/booking-history.html", bookings=bookings)

@mod.route('/admin/cars', methods=['GET'])
@requires_login
def admin_cars():
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    cars = Car.query.all()
    return render_template("users/admin/cars.html", cars=cars)

@mod.route('/admin/cars/create', methods=['GET', 'POST'])
@requires_login
def admin_cars_create():
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    form = CarForm(request.form)
    if form.validate_on_submit():
        car = Car(make=form.make.data, 
                  color=form.color.data,
                  body_type=form.body_type.data,
                  seats=form.seats.data,
                  cost_per_hour=form.cost_per_hour.data)
        # Insert the record in our database and commit it
        db.session.add(car)
        db.session.commit()
        flash('Car added.')
        return redirect(url_for('users.admin_cars_create'))
        # redirect user to the 'home' method of the user module.    
    return render_template("users/admin/cars-create.html", form=form)    

@mod.route('/admin/cars/edit/<car_id>', methods=['GET', 'POST'])
@requires_login
def admin_cars_edit(car_id):
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    car = Car.query.filter_by(id=car_id).first()
    if not car: 
        return "400 car not exists"
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        flash('Car information updated.')
    return render_template("users/admin/cars-edit.html", form=form)

@mod.route('/admin/cars/delete', methods=['POST'])
@requires_login
def admin_cars_delete():
    if not g.user.isAdmin():
        return "503 Not sufficent permission", 503
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        return '', 200
    return 'car not exist.', 404

@mod.route('/admin/cars/report', methods=['POST'])
@requires_login
def admin_cars_report():
    if not g.user.isAdmin():
        return "503 Not sufficent permission", 503
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        car_report = CarReport(car.id)
        db.session.add(car_report)
        db.session.commit()
        return '', 200
    return 'car not exist.', 404

@mod.route('/admin/users', methods=['GET'])
@requires_login
def admin_users():
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    users = User.query.all()
    return render_template("users/admin/users.html", users=users)

@mod.route('/admin/users/create', methods=['GET', 'POST'])
@requires_login
def admin_users_create():
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                  password=generate_password_hash(form.password.data),
                  email=form.email.data,
                  first_name=form.first_name.data,
                  last_name=form.last_name.data,
                  role=form.role.data)
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()
        flash('User added.')
        return redirect(url_for('users.admin_users_create'))
        # redirect user to the 'home' method of the user module.    
    return render_template("users/admin/users-create.html", form=form)    

@mod.route('/admin/users/edit/<user_id>', methods=['GET', 'POST'])
@requires_login
def admin_users_edit(user_id):
    if not g.user.isAdmin():
        return "503 Not sufficent permission"
    user = User.query.filter_by(id=user_id).first()
    if not user: 
        return "400 user not exists"
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User information updated.')
    return render_template("users/admin/users-edit.html", form=form)

@mod.route('/admin/users/delete', methods=['POST'])
@requires_login
def admin_users_delete():
    if not g.user.isAdmin():
        return "503 Not sufficent permission", 503
    user = User.query.filter_by(id=request.form['user_id']).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 200
    return 'user not exist.', 404

@api_mod.route('/login/', methods=['POST'])
def api_login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password, request.form['password']):
        return user.serialize(), 200
    else:
        return '{}', 401

def api_logout():
    pass