import socket
import json
import pickle
import datetime

PORT = 65000         
ADDRESS = ("", PORT)

def send_credentials(action, car_id, username, password=None):
    '''
    Send user login credentials to MP for authentication and 
    get result

    :args:
        -   action: 1 for username/password credentials
                    2 for facial recognition
        -   car_id: Car id
        -   username: username
        -   password: password if use action 1
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        credentials = {}
        if action == 1:
            credentials = {
                "action" : 1,
                "car_id" : car_id,
                "username" : username,
                "password" : password,
                "date" : datetime.datetime.now()
            } 
        else:
            credentials = {
                "action" : 2,
                "car_id" : car_id,
                "username" : username,
                "date" : datetime.datetime.now()
            } 
        s.sendall(pickle.dumps(credentials))
        response = s.recv(4096)
        response_dict = pickle.loads(response).json()
    return response_dict
