from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import action
import time

main_menu = None
user_menu = None

FORMAT = MenuFormatBuilder() \
            .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
            .set_prompt("SELECT>") \
            .set_title_align('center') \
            .set_subtitle_align('center') \
            .set_left_margin(8) \
            .set_right_margin(8) \
            .show_header_bottom_border(True)

def create_main_menu():
    menu = ConsoleMenu("Main menu", formatter=FORMAT)

    #Customer section
    customer_login_submenu = SelectionMenu([], 'Customer login',
        formatter=FORMAT)
    face_login_item = FunctionItem("Use username/password", 
        action.user_login_with_credentials)
    credentials_login_item = FunctionItem("Use facial recognition", 
        action._pass)
    customer_login_submenu.append_item(face_login_item)
    customer_login_submenu.append_item(credentials_login_item)

    #engineer section
    engineer_login_submenu = SelectionMenu([], 'Engineer login', 
        formatter=FORMAT)
    customer_login_item = SubmenuItem("Customer login", 
        customer_login_submenu, menu)
    engineer_login_item = SubmenuItem("Retrieve engineer's profile by QR code", 
        engineer_login_submenu, menu)

    menu.append_item(customer_login_item)
    menu.append_item(engineer_login_item)
    return menu

def create_user_menu():
    menu = ConsoleMenu("", formatter=FORMAT)
    logout_item = FunctionItem("Call for repair!!!", action._pass)
    menu.append_item(logout_item)
    return menu


main_menu = create_main_menu()
user_menu = create_user_menu()




