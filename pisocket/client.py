import socket
import json
import pickle

PORT = 65000         
ADDRESS = ("", PORT)

def send_credentials(action, username, password=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(ADDRESS)
        credentials = {}
        if action == 1:
            credentials = {
                "action" : 1,
                "username" : username,
                "password" : password
            } 
        else:
            credentials = {
                "action" : 2,
                "username" : username,
            } 
        s.sendall(pickle.dumps(credentials))
        response = s.recv(4096)
        response_dict = pickle.loads(response).json()
    return response_dict

if __name__ == '__main__':
    print(send_credentials(2, "trungngo"))