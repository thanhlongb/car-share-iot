#!/usr/bin/env python
import os
import readline
from pprint import pprint
from flask import *
from app import *
from app import db
import pymysql

pymysql.install_as_MySQLdb()
os.environ['PYTHONINSPECT'] = 'True'

def prompt_options():
    options = """Select an operation:
    1/ Create all tables.
    2/ Drop all tables.
    3/ Exit.\nYour option: """
    return int(input(options))

def create_all_tables():
    db.create_all()
    print('all tables created.')

def drop_all_tables():
    db.drop_all()
    print('all tables dropped.')

while True:
    option = prompt_options()
    if option == 1: create_all_tables()
    elif option == 2: drop_all_tables()
    elif option == 3: 
        exit("bye.")
        break
    else: print("invalid option. try again!")
    