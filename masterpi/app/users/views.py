import os, pickle, requests, json
import numpy as np
from json import JSONEncoder
import requests, json
import qrcode
import datetime
import jsonify

from json import JSONEncoder
from multiprocessing import Process
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, and_, desc, func
from werkzeug.utils import secure_filename
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Message

from app import db, login_manager, client, mail
from app.users.forms import RegisterForm, LoginForm, UserForm, UserEditForm, PhotosForm
from app.users.models import User
from app.cars.models import Car, CarReport
from app.cars.forms import CarForm
from app.bookings.models import Booking, BookingAction
from ..facial_recognition.encode_faces import encode
from ..charting.prepare_chart_data import get_line_chart_data, get_pie_chart_data, get_bar_chart_data

mod = Blueprint('users', __name__, url_prefix='/')
api_mod = Blueprint('users_api', __name__, url_prefix='/api')
FACE_UPLOAD_FOLDER_URL = 'app/facial_recognition/dataset'
QR_UPLOAD_FOLDER_URL = 'app/qr_code'

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

def generate_qr_code(old_engineer_name, new_engineer_name):
    print(old_engineer_name)
    if old_engineer_name != '':
        oldfilename = old_engineer_name + '.png'
        dir = os.path.join(QR_UPLOAD_FOLDER_URL, oldfilename)
        if os.path.exists(dir):
            os.remove(dir)
    
    newfilename = new_engineer_name + '.png'
    directory = os.path.join(QR_UPLOAD_FOLDER_URL, newfilename)
    img = qrcode.make(new_engineer_name)
    img.save(directory)
    
@login_manager.user_loader
def load_user(user_id):
    """ retrieve the user on the database using user id 

    :param int id: the id of user
    
    :return: return user object with corresponding user id
    :rtype: User
    """
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """ Redirect the user to login page if the user type is invalid
    """
    return redirect(url_for('users.login'))

@mod.route('/')
@login_required
def home():
    """ Redirect the user to home page which have booking history
    """
    bookings = Booking.query.filter_by(user_id=current_user.id) \
                            .order_by(Booking.id.desc()).all()
    return render_template("users/home.html", user=current_user, bookings=bookings)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """ This function login using register account
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.login_redirect'))
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
    """ Login form using Google account
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.login_redirect'))    
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
    """ retrieve user information in Google account
    """
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
        user = User(userinfo_response['email'],
                    username=userinfo_response['sub'], 
                    first_name=userinfo_response['given_name'],
                    last_name=userinfo_response['family_name'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('users.login_redirect'))

@mod.route('/login/redirect')
@login_required
def login_redirect():
    """ Redirect to page based on user role
    """
    if current_user.isEngineer():
        return redirect(url_for('users.engineer_reports'))
    if current_user.isManager():
        return redirect(url_for('users.dashboard'))
    if current_user.isAdmin():
        return redirect(url_for('users.admin_pages'))
    return redirect(url_for('users.home'))
 
@mod.route('/logout/')
@login_required
def logout():
    """ User logout 
    """
    logout_user()
    return redirect(url_for('users.login'))
  
@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """ Registration Form for register new account
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.login_redirect'))    
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # check whether if there is user with the same username/email
        user = User.query.filter(or_(User.username == form.username.data, 
                                     User.email == form.email.data)).first()
        if not user:
            # create an user instance not yet stored in the database
            user = User(form.email.data, 
                        username=form.username.data, 
                        first_name=form.first_name.data, 
                        last_name=form.last_name.data, 
                        password=generate_password_hash(form.password.data))
            # Insert the record in our database and commit it
            db.session.add(user)
            db.session.commit()

            # Log the user in, as he now has an id
            login_user(user)
            # redirect user to the 'home' method of the user module.
            return redirect(url_for('users.login_redirect'))
        flash('Username or email is taken.')
    return render_template("users/register.html", form=form)

@mod.route('/dashboard/')
@login_required
def dashboard():
    """ Redirect to dashboard
    """
    if not (current_user.isAdmin() or current_user.isManager()):
        return "503 Not sufficent permission"

    line_chart_data = get_line_chart_data()
    pie_chart_data = get_pie_chart_data()
    bar_chart_data = get_bar_chart_data()

    return render_template("users/dashboard.html", 
        line_chart_labels = line_chart_data['labels'],
        line_chart_values = line_chart_data['values'],
        pie_chart_labels = pie_chart_data['labels'],
        pie_chart_values = pie_chart_data['values'],
        bar_chart_labels = bar_chart_data['labels'],
        bar_chart_values = bar_chart_data['values']
    ) 
    
@mod.route('/engineer/')
@login_required
def engineer():
    """ Redirect to engineering page
    """
    return render_template("users/engineer.html")
  
@mod.route('/admin/bookings', methods=['GET'])
@login_required
def admin_bookings():
    """ Redirect the admin to booking page which show the list of bookings
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    bookings = Booking.query.order_by(desc(Booking.id)).all()
    return render_template("users/admin/bookings.html", bookings=bookings)

@mod.route('/admin/cars', methods=['GET'])
@login_required
def admin_cars():
    """ Redirect the admin to car page which show the list of cars
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    cars = Car.query.order_by(desc(Car.id)).all()
    return render_template("users/admin/cars.html", cars=cars)

@mod.route('/admin/cars/create', methods=['GET', 'POST'])
@login_required
def admin_cars_create():
    """ This function allow admin to create a car record in the database

        :reqheader Accept: application/json
        :param string make: car brand
        :param string color: car color
        :param string body_type: car body type
        :param int seats: number of seats
        :param int cost_per_hour: cost per hour
        
        :status 200: car created
        :status 400: bad request
    """
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
    """ Update car's properties

    :param int car_id: id of an existing car

    :status 200: car report updated
    :status 400: car not exist
    :status 503: Not sufficent permission

    """
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
    """ 
    This function allow admin to delete a car record in the database

        :param int car_id: id of the car

        :status 201: car deleted
        :status 404: car not exist
        :status 503: Not sufficent permission

    """
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
    """ This function allow admin to create a car report from the database

        :reqheader Accept: application/json
        :param int car_id: id of the car

        :status 200: car report created
        :status 400: car not exist
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission", 503
    car = Car.query.filter_by(id=request.form['car_id']).first()
    if car:
        car_report = CarReport(car.id)
        db.session.add(car_report)
        db.session.commit()
        return '', 200
    return 'car not exist.', 404

@mod.route('/manager/reports', methods=['GET'])
@login_required
def manager_reports():
    """ This function generate the report page of the user

        :status 200: OK
        :status 404: bad request
    """
    if not current_user.isManager():
        return "503 Not sufficent permission"
    reports = CarReport.query.filter_by(fixed=False).all()
    engineers = User.query.order_by(desc(User.id)).filter_by(role=2).all()
    return render_template("users/manager/reports.html", reports=reports, engineers=engineers)

@mod.route('/manager/reports/assign', methods=['POST'])
@login_required
def manager_reports_assign():
    """ This function will let manager assign task for engineer by sending HTTP POST methods

        :param str engineer_id: id of an existing engineering

        :status 200: OK
        :status 404: bad request
    """
    if not current_user.isManager():
        return "503 Not sufficent permission", 503
    report = CarReport.query.filter_by(id=request.form['report_id']).first()
    if report:
        report.fixer_id = request.form['engineer_id']
        db.session.commit()
        fixer = User.query.filter_by(id=request.form['engineer_id']).first()
        # send email to fixer
        email = Message("There is a new vehicle with issues reported!",
                        recipients=[fixer.email])
        mail.send(email)
        return '', 200
    return 'report not exist.', 404

@mod.route('/engineer/reports', methods=['GET'])
@login_required
def engineer_reports():
    """ This function generate the report page of the user

        :status 200: OK
        :status 404: bad request
    """
    if not current_user.isEngineer():
        return "503 Not sufficent permission"
    reports = CarReport.query.filter(and_(CarReport.fixed == False,
                                          CarReport.fixer_id == current_user.id)) \
                             .order_by(desc(CarReport.id)) \
                             .all()
    return render_template("users/engineer/reports.html", reports=reports)

@mod.route('/engineer/reports/fixed', methods=['POST'])
@login_required
def engineer_reports_fixed():
    """ This function will let manager assign task for engineer by sending HTTP POST methods

        :param str report_id: id of an existing engineering

        :status 200: OK
        :status 404: report not exist
    """
    if not current_user.isEngineer():
        return "503 Not sufficent permission", 503
    report = CarReport.query.filter_by(id=request.form['report_id']).first()
    if report:
        report.fixed = True
        db.session.commit()
        return '', 200
    return 'report not exist.', 404


@mod.route('/admin/pages', methods=['GET'])
@login_required
def admin_pages():
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    return render_template("users/admin/pages.html")

@mod.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    """ Redirect admin to user management page
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    users = User.query.order_by(desc(User.id)).all()
    return render_template("users/admin/users.html", users=users)

@mod.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def admin_users_create():
    """ This function allow admin to create a car report in the database

        :reqheader Accept: application/json
        :param str email: email of the user
        :param str username: username of the user
        :param str password: password of the user
        :param str first_name: first name
        :param str last_name: last name
        :param int role: role of user
        :param str bluetooth_MAC: mac address of user's bluetooth device

        :status 200: car report created
        :status 400: car not exist
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User(form.email.data,
                    username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    role=form.role.data,
                    bluetooth_MAC = form.bluetooth_MAC.data)
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        #Generate QR code
        if form.role.data == '2':
            generate_qr_code('', form.username.data)

        flash('User added.')
        return redirect(url_for('users.admin_users_create'))
        # redirect user to the 'home' method of the user module.    
    return render_template("users/admin/users-create.html", form=form)   

@mod.route('/admin/users/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def admin_users_edit(user_id):
    """ Edit an existing user

    :param int user_id: id of an existing user

    :status 200: User report updated
    :status 400: user not exist
    :status 503: Not sufficent permission
    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission"
    user = User.query.filter_by(id=user_id).first()
    if not user: 
        return "400 user not exists"
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()

        #generate new QR code
        if form.role.data == '2':
            generate_qr_code(user.getUsername(), form.username.data)
        
        flash('User information updated.')
    return render_template("users/admin/users-edit.html", form=form)

@mod.route('/admin/users/delete', methods=['POST'])
@login_required
def admin_users_delete():
    """ This function allow admin to delete an user record in the database

    :param int user_id: id of the user

    :status 201: user deleted
    :status 404: user not exist
    :status 503: Not sufficent permission

    """
    if not current_user.isAdmin():
        return "503 Not sufficent permission", 503
    user = User.query.filter_by(id=request.form['user_id']).first()
    if user:

        #delete qr_code
        if user.getRole() == 'engineer':
            filename = user.getUsername() + '.png'
            directory = os.path.join(QR_UPLOAD_FOLDER_URL, filename)
            if os.path.exists(directory):
                os.remove(directory)

        db.session.delete(user)
        db.session.commit()
        return '', 200
    return 'user not exist.', 404

################################ User unlock car ######################################
@api_mod.route('/login_by_credentials/', methods=['POST'])
def api_login_by_credentials():
    """ This function allow user to unlock car by using their account

    :param str username: user name of the user
    :param str password: password of the user

    :status 200: login success
    :status 401: login failed
    """

    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password, request.form['password']):
        car = Car.query.filter_by(id = request.form['car_id']).first()
        if car.booked and car.bookings[-1].user_id == user.id:
            bookingAction = BookingAction(car.bookings[-1].id, "unlocked")
            db.session.add(bookingAction)
            db.session.commit()
            return user.serialize(), 200
        return '{}', 401
    else:
        return '{}', 401

@api_mod.route('/login_by_facial_recognition/', methods=['POST'])
def api_login_by_facial_recognition():
    user = User.query.filter_by(username=request.form['username']).first()
    if user:
        car = Car.query.filter_by(id = request.form['car_id']).first()
        if car.booked and car.bookings[-1].user_id == user.id:
            bookingAction = BookingAction(car.bookings[-1].id, "unlocked")
            db.session.add(bookingAction)
            db.session.commit()
            return user.serialize(), 200
    else:
        return '{}', 401

@api_mod.route('/logout/', methods=['POST'])
def api_logout():
    car = Car.query.filter_by(id = request.form['car_id']).first()
    bookingAction = BookingAction(car.bookings[-1].id, "returned")
    db.session.add(bookingAction)
    db.session.commit()
    return '{}', 200

@api_mod.route('/face_encodings/', methods=['GET'])
def face_encodings():
    """ This function allow user to unlock car by using facial recognition

    :status 200: login success
    :status 401: login failed

    """
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
            user = User.query.filter_by(id=current_user.id).first()
            username = user.username
            directory = os.path.join(FACE_UPLOAD_FOLDER_URL, username)
            if not os.path.exists(directory):
                os.makedirs(directory)
            for f in request.files.getlist('images'):
                filename = secure_filename(f.filename)
                f.save(os.path.join(directory, filename))
            thread = Process(target=encode)
            thread.run()
            return render_template("users/photos-upload.html", form=form, uploaded=True)
    return render_template("users/photos-upload.html", form=form, uploaded=False)


################################ Engineer unlock car ######################################
@api_mod.route('/engineer_unlock_car_QR/', methods=['POST'])
def api_engineer_unlock_car_by_QR():
    """ This function allow user to unlock car by using QR code

    :status 200: login success
    :status 401: login failed

    """
    engineer = User.query.filter_by(username=request.form['username']).first()
    if engineer and engineer.isEngineer():
        return engineer.serialize(), 200
    else:
        return '{}', 401

@api_mod.route('/engineer_unlock_car_bluetooth/', methods=['POST'])
def api_engineer_unlock_car_by_bluetooth():
    """ This function allow user to unlock car by bluetooth

    :status 200: login success
    :status 401: login failed

    """
    engineer = User.query.filter_by(bluetooth_MAC=request.form['bluetooth_MAC']).first()
    if engineer and engineer.isEngineer():
        return engineer.serialize(), 200
    else:
        return '{}', 401
