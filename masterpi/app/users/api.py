import os, pickle, requests, json

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, and_, desc, func

from app import db, login_manager, client, mail
from app.users.forms import RegisterForm, LoginForm, UserForm, UserEditForm, PhotosForm
from app.users.models import User
from app.cars.models import Car, CarReport
from app.cars.forms import CarForm
from app.bookings.models import Booking, BookingAction

api_mod = Blueprint('user', __name__, url_prefix='/api')

@api_mod.route('/users/', methods=['GET'])
def get_users():
    users = User.query.order_by(desc(User.id)).all()
    data = [r.serialize() for r in users]
    return jsonify(data)

@api_mod.route('/users/create/', methods=['POST'])
def users_create():
    form = RegisterForm(request.form)
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
        return user.serialize()
    return {}, 401

@api_mod.route('/users/edit/<user_id>', methods=['POST'])
def users_update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user: 
        return "400 user not exists"
    form = UserEditForm(request.form)
    form.populate_obj(user)
    db.session.commit()
    return user.serialize(), 200

@api_mod.route('/users/delete', methods=['DELETE'])
def users_delete():
    user = User.query.filter_by(id=request.form['user_id']).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return user.serialize(), 200
    return 'user not exist.', 404