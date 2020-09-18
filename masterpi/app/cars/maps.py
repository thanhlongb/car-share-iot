import geocoder
from flask_googlemaps import  Map, icons

class StaticMap:
    DEFAULT_MARKER = "https://img.icons8.com/color/48/000000/car.png"
    main_location = None
    locations = []
    """
    This class will create a Map object which hold the location of the car
    """
    def __init__(self, name, lat, long):
        """
        This function is the constructor

        :param str locationName: the name of the current location
        """
        self.main_location = (name, lat, long)
        self.add_location(name, lat, long)

    def add_location(self, name, lat, long):
        self.locations.append((name, lat, long))

    def get_location_coordinate(self, location):
        """ 
        This function call the geolocation API of ArcGIS to get the lattitude and longtitude from the location name

        :return:  the lattitude and longtitude of the given location
        :rtype: list
        """
        g = geocoder.arcgis(location)
        return g.latlng

    def generate_markers(self):
        markers = []
        for location in self.locations:
            markers.append({
                "icon": self.DEFAULT_MARKER,
                "infobox": location[0],
                "lat": location[1],
                "lng": location[2]
            })
        return markers

    def create_map(self):
        """
        This function create a Map object contain location of the car

        :return: a Map object
        :rtype: Map
        """
        carMap = Map(
            identifier="carMap",
            varname="carMap",
            lat=self.main_location[1],
            lng=self.main_location[2],
            markers=self.generate_markers(),
            style="height:400px;width:100%;margin:0;",
        )
        return carMap