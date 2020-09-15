import geocoder
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map, icons

@app.route("/")
def map_created_in_view():

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=10.78403000000003,
        lng=106.69434000000007,
        markers={
            # icons.dots.green: [(21.02988000000005, 105.81131000000005)],
            icons.dots.blue: [(10.78403000000003, 106.69434000000007, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)

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
        googleMap = Map(
            identifier="car location",
            varname="gmap",
            lat=geolocation[0],
            lng=geolocation[1],
            markers={
                icons.dots.blue: [(10.78403000000003, 106.69434000000007, description)],
            },
            style="height:400px;width:600px;margin:0;",
        )
        return googleMap