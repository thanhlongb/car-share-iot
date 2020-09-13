import socket
import requests
import pickle
import json

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
            response = requests.post("https://127.0.0.1:5000/api/users/login/", credentials, verify=False)
            print("Sending data back.")
            conn.sendall(pickle.dumps(response))
            print("Disconnecting from client.")
        
        print("Closing listening socket.")
    print("Done.")
