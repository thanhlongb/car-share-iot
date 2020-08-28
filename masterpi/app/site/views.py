from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

mod = Blueprint('site', __name__, url_prefix='/')

@mod.route('/', methods=['GET'])
def home():
    return render_template("home.html")

