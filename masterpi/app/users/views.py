import os, pickle, requests, json
import numpy as np
from multiprocessing import Process
from json import JSONEncoder
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import db, login_manager, client
from app.users.forms import RegisterForm, LoginForm, UserForm, UserEditForm, PhotosForm
# from ..facial_recognition.encode_faces import encode
from app.users.models import User
from app.cars.models import Car, CarReport
from app.cars.forms import CarForm
from app.bookings.models import Booking

mod = Blueprint('users', __name__, url_prefix='/users')
api_mod = Blueprint('users_api', __name__, url_prefix='/api/users')
UPLOAD_FOLDER_URL = 'app/facial_recognition/dataset'

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

@mod.route('/login/redirect')
@login_required
def login_redirect():
    if current_user.isEngineer():
        return redirect(url_for('users.engineer'))
    if current_user.isManager() or current_user.isAdmin():
        return redirect(url_for('users.dashboard'))
    return redirect(url_for('users.home'))

@mod.route('/')
@login_required
def home():
    bookings = Booking.query.filter_by(user_id=current_user.id) \
                            .order_by(Booking.id.desc()).all()
    return render_template("users/home.html", user=current_user, bookings=bookings)
    
@mod.route('/dashboard/')
@login_required
def dashboard():
    return render_template("users/dashboard.html")
    
@mod.route('/engineer/')
@login_required
def engineer():
    return render_template("users/engineer.html")
    

@mod.route('/logout/')
@login_required
def logout():
    session['user_id'] = None
    return redirect(url_for('users.login'))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# @mod.before_request
# def before_request():
#     """
#     pull user's profile from the database before every request are treated
#     """
#     current_user = None
#     if 'user_id' in session:
#         current_user = User.query.get(session['user_id'])

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
            login_user(user)
            return redirect(url_for('users.login_redirect'))
        flash('Wrong username or password', 'error-message')
    return render_template("users/login.html", form=form)

@mod.route('/google-login/', methods=['GET'])
def google_login():
    #ref: https://realpython.com/flask-google-login/
    #TODO: check if user's is logged in
    google_provider_cfg = requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('users.google_callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@mod.route('/google-login/callback', methods=['GET'])
def google_callback():
    #ref: https://realpython.com/flask-google-login/
    code = request.args.get("code")
    google_provider_cfg = requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['GOOGLE_CLIENT_ID'], 
              current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body).json()
    user = User.query.filter_by(email=userinfo_response['email']).first()
    if not user:
        user = User.google_init(userinfo_response['sub'],
                                userinfo_response['email'], 
                                first_name=userinfo_response['given_name'],
                                last_name=userinfo_response['family_name'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('users.login_redirect'))

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
            login_user(user)
            # redirect user to the 'home' method of the user module.
            return redirect(url_for('users.login_redirect'))
        flash('Email address or username is taken.')
    return render_template("users/register.html", form=form)
    
@mod.route('/booking-history/', methods=['GET'])
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template("users/booking-history.html", bookings=bookings)

@mod.route('/admin/bookings', methods=['GET'])
@login_required
def admin_bookings():
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    bookings = Booking.query.all()
    return render_template("users/admin/bookings.html", bookings=bookings)


@mod.route('/admin/cars', methods=['GET'])
@login_required
def admin_cars():
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    cars = Car.query.all()
    return render_template("users/admin/cars.html", cars=cars)

@mod.route('/admin/cars/create', methods=['GET', 'POST'])
@login_required
def admin_cars_create():
    if not current_user.isAdmin():
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
@login_required
def admin_cars_edit(car_id):
    if not current_user.isAdmin():
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
@login_required
def admin_cars_delete():
    if not current_user.isAdmin():
        return "503 Not sufficent permission", 503
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        return '', 200
    return 'car not exist.', 404

@mod.route('/admin/cars/report', methods=['POST'])
@login_required
def admin_cars_report():
    if not current_user.isAdmin():
        return "503 Not sufficent permission", 503
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        car_report = CarReport(car.id)
        db.session.add(car_report)
        db.session.commit()
        return '', 200
    return 'car not exist.', 404

@mod.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    users = User.query.all()
    return render_template("users/admin/users.html", users=users)

@mod.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def admin_users_create():
    if not current_user.isAdmin():
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
@login_required
def admin_users_edit(user_id):
    if not current_user.isAdmin():
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
@login_required
def admin_users_delete():
    if not current_user.isAdmin():
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

@api_mod.route('/face_encodings/', methods=['GET'])
def face_encodings():
    encodings = pickle.loads(open('app/facial_recognition/output/encodings.pickle', 'rb').read())
    encodings_json = json.dumps(encodings, cls=NumpyArrayEncoder)
    return encodings_json

@mod.route('/photos-upload/', methods=['GET', 'POST'])
@login_required
def photos_upload():
    """
    Upload photos
    """
    form = PhotosForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=session['user_id']).first()
            username = user.username
            directory = os.path.join(UPLOAD_FOLDER_URL, username)
            if not os.path.exists(directory):
                os.makedirs(directory)
            for f in request.files.getlist('images'):
                filename = secure_filename(f.filename)
                f.save(os.path.join(directory, filename))
            thread = Process(target=encode)
            thread.run()
            return render_template("users/photos-upload.html", form=form, uploaded=True)
    return render_template("users/photos-upload.html", form=form, uploaded=False)