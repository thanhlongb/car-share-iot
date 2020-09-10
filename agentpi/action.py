import os.path
import sys
import time
import menu
import getpass
import requests
import pickle
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from facial_recognition.train_model import train_model
from facial_recognition.recognize import recognize
from qr_code import get_QR_encryption
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from pisocket import client

GET_FACE_ENCODINGS_API = "https://127.0.0.1:5000/api/users/face_encodings/"
ENGINEER_LOGIN_BY_QR_CODE_API = "https://127.0.0.1:5000/api/users/engineer_unlock_car_QR/"
warnings.simplefilter('ignore',InsecureRequestWarning)

def _pass():
    pass

def user_logout():
    #TODO: change availability of the car in the db
    menu.user_menu.exit()

##-------------------------------- User login with credentials --------------------------------##
def handle_fail_user_login(use_credentials):
    if use_credentials:
        print("Wrong username/password! Please try again.")
    else:
        print("Cannot recognize user's face! Please try again.")
    time.sleep(2)
    menu.main_menu.resume()

def handle_success_user_login(username):
    print("\n\nWelcome user '{}' to the car".format(username))
    time.sleep(2)
    menu.main_menu.pause()
    menu.user_menu.title = username
    menu.user_menu.show()

def user_login_with_credentials():
    menu.main_menu.pause()
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    res_dict = client.send_credentials(username, password)
    if len(res_dict) == 0:
        handle_fail_user_login(use_credentials=True)
    else:
        handle_success_user_login(username=res_dict['username'])

##-------------------------------- User login with facial recognition --------------------------------##
def update_facial_encodings():
    print('[INFO] Updating face encodings from server...')
    response = requests.get(GET_FACE_ENCODINGS_API, verify=False)
    response_pickle = response.json()
    return response_pickle

def handle_facial_recognition_result(username):
    if username == 'unknown':
        handle_fail_user_login(use_credentials=False)
    else:
        handle_success_user_login(username)

def user_login_with_facial_recognition():
    menu.main_menu.pause()
    new_encodings_data = update_facial_encodings()
    print('[INFO] Training new model...')
    train_model(new_encodings_data)
    print('[INFO] Initializing...')
    username = recognize()
    handle_facial_recognition_result(username)

##-------------------------------- Engineer login with QR code --------------------------------##
def handle_fail_engineer_login():
    print('The QR code used is invalid. Please try again!')
    time.sleep(2)
    menu.main_menu.resume()

def handle_success_engineer_login(engineer_username):
    print("\n\nWelcome engineer '{}' to the car".format(engineer_username))
    time.sleep(2)
    menu.main_menu.pause()
    menu.engineer_menu.title = engineer_username
    menu.engineer_menu.show()

def engineer_login_with_QR_code():
    engineer_username = get_QR_encryption()
    Params = {'username' : engineer_username}
    response = requests.post(ENGINEER_LOGIN_BY_QR_CODE_API, Params, verify=False)
    response_json = response.json()
    if len(response_json) != 0:
        handle_success_engineer_login(response_json['username'])
    else:
        handle_fail_engineer_login()

if __name__ == '__main__':
    engineer_login_with_QR_code()


