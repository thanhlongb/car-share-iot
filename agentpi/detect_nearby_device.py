import warnings
import bluetooth
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
ENGINEER_LOGIN_BY_BLUETOOTH_API = "https://127.0.0.1:5000/api/engineer_unlock_car_bluetooth/"

def detect():
    """
	Detect nearby Bluetooth devices, get its
    bluetooth MAC and send to MP for 

    :return: - username if sucessfully authenticated.
             - empty string otherwise.
    """
    nearbyDevices = bluetooth.discover_devices()
    for macAddress in nearbyDevices:
        if macAddress != '':
            Params = {'bluetooth_MAC' : macAddress}
            response = requests.post(ENGINEER_LOGIN_BY_BLUETOOTH_API, Params, verify=False)
            response_json = response.json()
            if len(response_json) != 0:
                return response_json['username']
    return ''
