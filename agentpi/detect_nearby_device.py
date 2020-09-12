import bluetooth
import time

ENGINEER_LOGIN_BY_BLUETOOTH_API = "https://127.0.0.1:5000/api/users/engineer_unlock_car_bluetooth/"

def detect():
    nearbyDevices = bluetooth.discover_devices()
    for macAddress in nearbyDevices:
        Params = {'username' : macAddress}
        response = requests.post(ENGINEER_LOGIN_BY_BLUETOOTH_API, Params, verify=False)
        response_json = response.json()
        if len(response_json) != 0:
            return response_json
    return ''
    # while True:
    #     nearbyDevices = bluetooth.discover_devices()
    #     for macAddress in nearbyDevices:
    #         Params = {'username' : macAddress}
    #         response = requests.post(ENGINEER_LOGIN_BY_BLUETOOTH_API, Params, verify=False)
    #         response_json = response.json()
    #         if len(response_json) != 0:
    #             print(response_json)
    #             return response_json

    #     time.sleep(3)

# if __name__ == '__main__':
#     detect()
