import time
import threading
import os.path
import sys
import getpass
import warnings
import requests
from pynput.keyboard import Key, Controller
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from facial_recognition.train_model import train_model
from facial_recognition.recognize import recognize
from qr_code import get_QR_encryption
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from pisocket import client
from detect_nearby_device import detect

GET_FACE_ENCODINGS_API = "https://0.0.0.0:5000/api/face_encodings/"
ENGINEER_LOGIN_BY_QR_CODE_API = "https://0.0.0.0:5000/api/engineer_unlock_car_QR/"
LOGOUT_API = "https://0.0.0.0:5000/api/logout/"
warnings.simplefilter('ignore',InsecureRequestWarning)
CAR_LOCKED = True
PROGRAM_EXIT = False
CAR_ID = 4

#--------------------------------- Menu ---------------------------------#
FORMAT = MenuFormatBuilder() \
            .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
            .set_prompt("SELECT>") \
            .set_title_align('center') \
            .set_subtitle_align('center') \
            .set_left_margin(8) \
            .set_right_margin(8) \
            .show_header_bottom_border(True)

#----- User menu -----#
def create_user_menu():
    """
    Create customer menu

    :return: usermenu as a ConoleMenu object
    """
    menu = ConsoleMenu("",
        formatter=FORMAT,
        show_exit_option=False,
    )
    exit_item = FunctionItem("Logout and lock car",
        user_logout,
        should_exit=True
    )
    menu.append_item(exit_item)
    return menu

#----- Engineer menu -----#
def create_engineer_menu():
    """
    Create engineer menu

    :return: engineermenu as a ConoleMenu object
    """
    menu = ConsoleMenu("",
        formatter=FORMAT,
        show_exit_option=False,
        exit_option_text="Logout and lock car"
    )
    exit_item = FunctionItem("Logout and lock car",
        engineer_logout,
        should_exit=True
    )
    menu.append_item(exit_item)
    return menu

#----- Main menu -----#
def create_main_menu(user_menu, engineer_menu):
    """
    Create engineer menu

    :args:   - user_menu : customer menu object
             - engineer_menu : engineer menu object

    :return: main menu as a ConsoleMenu objects
    """
    menu = ConsoleMenu(
        "Main menu | Car locked",
        formatter=FORMAT,
        show_exit_option=False
    )

    #Customer section
    customer_login_submenu = SelectionMenu([],
        'Customer login | Car locked',
        formatter=FORMAT,
        exit_option_text="Return to Main menu"
    )
    credentials_login_item = FunctionItem("Use username/password",
        user_login_with_credentials,
        menu=customer_login_submenu,
        args=(menu, user_menu),
    )
    facial_login_item = FunctionItem("Use facial recognition",
        user_login_with_facial_recognition,
        menu=customer_login_submenu,
        args=(menu, user_menu)
    )
    customer_login_submenu.append_item(facial_login_item)
    customer_login_submenu.append_item(credentials_login_item)
    customer_login_submenu_item = SubmenuItem("Customer login",
        customer_login_submenu,
        menu
    )

    #engineer section
    engineer_login_submenu = SelectionMenu([],
        'Engineer login | Car locked',
        formatter=FORMAT,
        exit_option_text="Return to Main menu"
    )
    QR_code_login_item = FunctionItem("Use QR code",
        engineer_login_with_QR_code,
        menu=engineer_login_submenu,
        args=(menu, engineer_menu)
    )
    engineer_login_submenu.append_item(QR_code_login_item)
    engineer_login_submenu_item = SubmenuItem(
        "Engineer login",
        engineer_login_submenu,
        menu
    )

    exit_item = FunctionItem("Exit",
        shutdown,
        should_exit=True
    )

    menu.append_item(customer_login_submenu_item)
    menu.append_item(engineer_login_submenu_item)
    menu.append_item(exit_item)
    return menu

#--------------------------------- Action ---------------------------------#
#---- User logout ----#
def user_logout():
    """
    Customer logout, create return action and save to database
    through MP API
    """
    global CAR_LOCKED
    CAR_LOCKED = True
    param = {
        "car_id" : CAR_ID
    }
    requests.post(LOGOUT_API, param ,verify=False)

def engineer_logout():
    """
    Engineer logout
    """
    global CAR_LOCKED
    CAR_LOCKED = True

def shutdown():
    """
    Console application shutdown
    """
    global PROGRAM_EXIT
    PROGRAM_EXIT = True

#---- User login with credentials ----#
def handle_fail_user_login(use_credentials, main_menu):
    """
    Handle when customer's login information is wrong

    :args:
        -   user_credentials: Customer's login credentials
        -   main_menu: Main menu object
    """
    if use_credentials:
        print("Wrong username/password! Please try again.")
    else:
        print("Cannot recognize user's face! Please try again.")
    time.sleep(2)
    global CAR_LOCKED
    CAR_LOCKED = True
    main_menu.resume()

def handle_success_user_login(username, user_menu):
    """
    Handle when customer's login information is right
    :args:
        -   user_credentials: Customer's login credentials
        -   main_menu: Main menu object
    """
    print("\n\nWelcome user '{}' to the car".format(username))
    time.sleep(2)
    user_menu.title = username + ' | Car unlocked'
    user_menu.show()

def user_login_with_credentials(main_menu, user_menu):
    """
    Handle customer login by credentials option
    :args:
        -   main_menu: Main menu object
        -   user_menu: User menu object
    """
    global CAR_LOCKED
    CAR_LOCKED = False
    main_menu.pause()
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    res_dict = client.send_credentials(1, CAR_ID, username, password)
    if len(res_dict) == 0:
        handle_fail_user_login(True, main_menu)
    else:
        handle_success_user_login(res_dict['username'], user_menu)

#---- User login with facial recognition 3----#
def update_facial_encodings():
    """
    Call MP API to update encodings.pickle
    :return:
        -   response_pickle: face encodings as dict
    """
    print('[INFO] Updating face encodings from server...')
    response = requests.get(GET_FACE_ENCODINGS_API, verify=False)
    response_pickle = response.json()
    return response_pickle

def handle_facial_recognition_result(username, main_menu, user_menu):
    """
    Handle the result of facial recognition
    :args:
        -   username:   username of recognized user
        -   main_menu:  Main menu object
        -   user_menu:  User menu object
    """
    if username == 'unknown':
        handle_fail_user_login(False, main_menu)
    else:
        res_dict = client.send_credentials(2, CAR_ID, username)
        if len(res_dict) == 0:
            handle_fail_user_login(False, main_menu)
        else:
            handle_success_user_login(username, user_menu)

def user_login_with_facial_recognition(main_menu, user_menu):
    """
    Process of user login by facial recognition
    :args:
        -   main_menu:  Main menu object
        -   user_menu:  User menu object
    """
    global CAR_LOCKED
    CAR_LOCKED = False
    main_menu.pause()
    new_encodings_data = update_facial_encodings()
    print('[INFO] Training new model...')
    train_model(new_encodings_data)
    print('[INFO] Initializing...')
    username = recognize()
    handle_facial_recognition_result(username, main_menu, user_menu)

#---- Engineer login with QR code ----#
def handle_fail_engineer_login(main_menu):
    """
    Handle fail engineer login
    :args:
        -   main_menu: Main menu object
    """
    global CAR_LOCKED
    CAR_LOCKED = True
    print('The QR code used is invalid. Please try again!')
    time.sleep(2)
    main_menu.resume()

def handle_success_engineer_login(engineer_username, engineer_menu):
    """
    Handle successful engineer login
    :args:
        -   engineer_username: engineer's username
        -   engineer_menu: Engineer menu object
    """
    global CAR_LOCKED
    CAR_LOCKED = False
    print("\n\nWelcome engineer '{}' to the car".format(engineer_username))
    time.sleep(2)
    tempMenu = ConsoleMenu.currently_active_menu
    tempMenu.pause()
    keyboard = Controller()
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    engineer_menu.title = engineer_username  + ' | Car unlocked'
    engineer_menu.start()
    engineer_menu.join()
    tempMenu.resume()

def engineer_login_with_QR_code(main_menu, engineer_menu):
    """
    Process of engineer login by scanning QR code
    :args:
        -   main_menu: Main menu object
        -   engineer_menu: Engineer menu object
    """
    global CAR_LOCKED
    CAR_LOCKED = False
    engineer_username = get_QR_encryption()
    Params = {'username' : engineer_username}
    response = requests.post(ENGINEER_LOGIN_BY_QR_CODE_API, Params, verify=False)
    response_json = response.json()
    if len(response_json) != 0:
        handle_success_engineer_login(response_json['username'], engineer_menu)
    else:
        handle_fail_engineer_login(main_menu)

def detect_bluetooth_device(main_menu, engineer_menu):
    """
    Automatically detect nearby Bluetooth devices and check
    if it belongs to an engineer.
    :args:
        -   main_menu: Main menu object
        -   engineer_menu: Engineer menu object
    """
    while True:
        global PROGRAM_EXIT
        global CAR_LOCKED
        if PROGRAM_EXIT:
            return
        if CAR_LOCKED:
            engineer_username = detect()
            if engineer_username != '':
                handle_success_engineer_login(engineer_username, engineer_menu)
        time.sleep(5)

if __name__ == '__main__':
    """
    Main program
    """
    user_menu = create_user_menu()
    engineer_menu = create_engineer_menu()
    main_menu = create_main_menu(user_menu, engineer_menu)
    bluetooth_device_detector = threading.Thread(
        target=detect_bluetooth_device,
        args=(main_menu, engineer_menu, ),
    )
    main_menu.start()
    bluetooth_device_detector.start()
    main_menu.join()
    bluetooth_device_detector.join()
