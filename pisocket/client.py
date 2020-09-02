import socket
import json
import pickle

PORT = 65000         
ADDRESS = ("", PORT)

def send_credentials(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        credentials = {
            "username" : username,
            "password" : password
        }
        s.sendall(pickle.dumps(credentials))
        response = s.recv(4096)
        response_dict = pickle.loads(response).json()
    return response_dict
