CITY_COORDINATES = {

    "Hyderabad": {
        "lat": 17.3850,
        "lng": 78.4867
    },

    "Goa": {
        "lat": 15.2993,
        "lng": 74.1240
    },

    "Delhi": {
        "lat": 28.6139,
        "lng": 77.2090
    }
}


class LocationService:

    @staticmethod
    def get_coordinates(city):

        return CITY_COORDINATES.get(city)