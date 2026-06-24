import requests
from decouple import config


class GooglePlacesService:

    API_KEY = config("GOOGLE_MAPS_API_KEY")

    @classmethod
    def search_places(cls, destination, query):

        url = (
            "https://maps.googleapis.com/maps/api/place/textsearch/json"
        )

        params = {
            "query": f"{query} in {destination}",
            "key": cls.API_KEY
        }

        response = requests.get(
            url,
            params=params
        )

        return response.json()