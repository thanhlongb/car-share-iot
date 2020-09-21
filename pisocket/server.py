import socket
import requests
import pickle
import json

def activate():
    '''
    Socket server which receives user's login credentials from 
    client socket to authenticate and send back fail/success result.
    '''
    HOST = ""    
    PORT = 65000 
    ADDRESS = (HOST, PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(ADDRESS)
        s.listen()

        print("Listening on {}...".format(ADDRESS))
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connected to {}".format(addr))
                data = conn.recv(4096)
                credentials = pickle.loads(data)
                if credentials['action'] == 1:
                    response = requests.post(
                        "https://127.0.0.1:5000/api/login_by_credentials/",
                        credentials,
                        verify=False
                    )
                else:
                    response = requests.post(
                        "https://127.0.0.1:5000/api/login_by_facial_recognition/",
                        credentials,
                        verify=False
                )
                print("Sending data back.")
                conn.sendall(pickle.dumps(response))
                print("Disconnecting from client.")

            print("Closing listening socket.")
        print("Done.")

if __name__ == '__main__':
    activate()
