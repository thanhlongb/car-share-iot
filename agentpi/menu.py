from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import action
import time

FORMAT = MenuFormatBuilder() \
            .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
            .set_prompt("SELECT>") \
            .set_title_align('center') \
            .set_subtitle_align('center') \
            .set_left_margin(8) \
            .set_right_margin(8) \
            .show_header_bottom_border(True)

def create_main_menu():
    menu = ConsoleMenu("Main menu", formatter=FORMAT, show_exit_option=False)

    #Customer section
    customer_login_submenu = SelectionMenu([], 'Customer login',
        formatter=FORMAT)
    credentials_login_item = FunctionItem("Use username/password", 
        action.user_login_with_credentials)
    facial_login_item = FunctionItem("Use facial recognition", 
        action.user_login_with_facial_recognition)
    customer_login_submenu.append_item(facial_login_item)
    customer_login_submenu.append_item(credentials_login_item)
    customer_login_submenu_item = SubmenuItem("Customer login", customer_login_submenu, menu)

    #engineer section
    engineer_login_submenu = SelectionMenu([], 'Engineer login', 
        formatter=FORMAT)
    QR_code_login_item = FunctionItem("Use QR code", 
        action.engineer_login_with_QR_code)
    engineer_login_submenu.append_item(QR_code_login_item)
    engineer_login_submenu_item = SubmenuItem("Engineer login", engineer_login_submenu, menu)

    exit_item = FunctionItem("Exit", 
        action._exitt)
    menu.append_item(customer_login_submenu_item)
    menu.append_item(engineer_login_submenu_item)
    menu.append_item(exit_item)
    return menu

def create_user_menu():
    menu = ConsoleMenu("", formatter=FORMAT, show_exit_option=False)
    call_for_repair_item = FunctionItem("Call for repair!!!", action._pass)
    logout_item = FunctionItem("Logout", action.user_logout)
    menu.append_item(call_for_repair_item)
    menu.append_item(logout_item)
    return menu

def create_engineer_menu():
    menu = ConsoleMenu("", formatter=FORMAT, show_exit_option=False)
    logout_item = FunctionItem("Logout", action.user_logout)
    menu.append_item(logout_item)
    return menu

class Menu:
    main_menu = create_main_menu()
    user_menu = create_user_menu()
    engineer_menu = create_engineer_menu()

    # @classmethod    
    # def __init__(self):
    #     if Menu.__instance != None:
    #         raise Exception("This class is a singleton!")
    #     else:
    #         Menu.__instance = self
            

    # def getMainMenu(self):
    #     return self.main_menu







