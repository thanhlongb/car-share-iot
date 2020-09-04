import os
import pickle
import json
import numpy as np
from json import JSONEncoder
from multiprocessing import Process
from ..facial_recognition.encode_faces import encode
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app import db
from app.users.forms import RegisterForm, LoginForm, PhotosForm
from app.users.models import User
from app.bookings.models import Booking
from app.users.decorators import requires_login

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
@requires_login
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