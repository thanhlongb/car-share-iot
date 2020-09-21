"""
.. module:: carMaps
   :synopsis: Create google maps object

"""
import geocoder
from flask_googlemaps import  Map, icons

class StaticMap:
    """
    This class will create a Map object which hold the location of the car
    """
    def __init__(self, locationName, car_id):
        """
        This function is the constructor

        :param str locationName: the name of the current location
        :param int car_id: the id of the car
        """
        self.locationName = locationName
        self.car_id = car_id


    def get_location_coordinate(self):
        """ 
        This function call the geolocation API of ArcGIS to get the lattitude and longtitude from the location name

        :return:  the lattitude and longtitude of the given location
        :rtype: list
        """
        g = geocoder.arcgis(self.locationName)
        return g.latlng


    def create_map(self):
        """
        This function create a Map object contain location of the car

        :return: a Map object
        :rtype: Map
        """
        geolocation = self.get_location_coordinate()
        description = "car {}".format(self.car_id)
        carMap = Map(
            identifier="carMap",
            varname="carMap",
            lat=geolocation[0],
            lng=geolocation[1],
            markers={
                icons.dots.blue: [(geolocation[0], geolocation[1], description)],
            },
            style="height:400px;width:600px;margin:0;",
        )
        return carMap