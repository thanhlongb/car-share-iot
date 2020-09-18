import requests, json
from flask import current_app

def get_current_location_coordinate():
    url = current_app.config['GOOGLE_GEOLOCATION_API_URL']
    url_params = {"key": current_app.config['GOOGLE_API_KEY']}
    url = url.format(**url_params)
    data = json.dumps({"considerIp": True})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=data, headers=headers).json()
    return response['location']

def get_current_location_name(lat, lng):
    url = current_app.config['GOOGLE_GEOCODING_API_URL']
    url_params = {"key": current_app.config['GOOGLE_API_KEY'],
                "lat": lat,
                "long": lng}
    url = url.format(**url_params)
    response = requests.post(url).json()
    return response['results'][0]['formatted_address']
