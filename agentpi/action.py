import os.path
import sys
import time
import menu
import getpass
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from pisocket import client

def _pass():
    pass

def user_logout():
    #TODO: change availability of the car in the db
    menu.user_menu.exit()

def handle_fail_user_login(use_credentials):
    print("Wrong username/password! Please try again.")
    time.sleep(2)
    menu.main_menu.resume()

def handle_success_user_login(use_credentials, username):
    print("\n\nWelcome '{}' to the car".format(username))
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
        handle_success_user_login(use_credentials=True, 
            username=res_dict['username'])