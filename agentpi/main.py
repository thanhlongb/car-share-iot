import time
from menu import Menu
from multiprocessing import Process, Pool, Queue, Process
import threading
import time
from detect_nearby_device import detect

class Main(object):
    engineer_nearby_username = ''
    engineer_logged_in = False
    program_exit = False

def process1():
    Menu.main_menu.show()
    

def process2():
    # if engineer_nearby_username == '' \
    #     and engineer_logged_in == False \
    #     and program_exit == False:
    # engineer_nearby_username = detect()
    while True:
        if Main.program_exit:
            return
        print('ccc')
        time.sleep(1)

# def run_process(process):
#     process()

if __name__ == '__main__':
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t1.start()
    t2.start()
