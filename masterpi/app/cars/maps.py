import geocoder
from flask_googlemaps import  Map, icons

class StaticMap:
    
    def __init__(self, locationName, car_id):
        self.locationName = locationName
        self.car_id = car_id


    def get_location_coordinate(self):
        g = geocoder.arcgis(self.locationName)
        return g.latlng


    def create_map(self):
        geolocation = self.get_location_coordinate()
        description = "car {}".format(car_id)
        gmap = Map(
            identifier="car location",
            varname="gmap",
            lat=geolocation[0],
            lng=geolocation[1],
            markers={
                icons.dots.blue: [(10.78403000000003, 106.69434000000007, description)],
            },
            style="height:400px;width:600px;margin:0;",
        )
        return gmap