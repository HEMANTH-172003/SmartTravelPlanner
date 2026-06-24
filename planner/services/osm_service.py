import requests
import time
import random

from .wikipedia_service import WikipediaService
from planner.services.wikipedia_service import WikipediaService

class OSMService:

    USER_AGENT = "SmartTravelPlanner/1.0"
    COORDINATE_CACHE = {}


    @staticmethod
    def get_coordinates(place):

        if place in OSMService.COORDINATE_CACHE:
            return OSMService.COORDINATE_CACHE[place]

        try:
            url = "https://nominatim.openstreetmap.org/search"

            params = {
                "q": place,
                "format": "json",
                "limit": 1
            }

            headers = {
                "User-Agent": OSMService.USER_AGENT
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            coordinates = {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }

            OSMService.COORDINATE_CACHE[place] = coordinates

            return coordinates

        except Exception as e:
            print(f"Nominatim Error: {e}")
            return None

    @staticmethod
    def _execute_overpass_query(query):

        overpass_urls = [
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://lz4.overpass-api.de/api/interpreter"
        ]

        for url in overpass_urls:

            for attempt in range(3):

                try:

                    response = requests.post(
                        url,
                        data=query,
                        headers={
                            "User-Agent": OSMService.USER_AGENT
                        },
                        timeout=120
                    )

                    response.raise_for_status()

                    return response.json()

                except Exception as e:

                    print(
                        f"{url} attempt {attempt + 1} failed: {e}"
                    )

                    time.sleep(5)

            print(
                "Switching to next Overpass server..."
            )

            time.sleep(2)

        return {"elements": []}

    @staticmethod
    def generate_map_link(lat, lon):

        if lat is None or lon is None:
            return None

        return (
            f"https://www.google.com/maps/search/"
            f"?api=1&query={lat},{lon}"
        )

    @staticmethod
    def get_hotels(destination):

        coordinates = OSMService.get_coordinates(
            destination
        )

        if not coordinates:
            return []

        lat = coordinates["lat"]
        lon = coordinates["lon"]

        query = f"""
        [out:json];
        (
          node["tourism"~"hotel|guest_house|hostel|motel"](around:15000,{lat},{lon});
          way["tourism"~"hotel|guest_house|hostel|motel"](around:15000,{lat},{lon});
          relation["tourism"~"hotel|guest_house|hostel|motel"](around:15000,{lat},{lon});
        );
        out center;
        """

        data = OSMService._execute_overpass_query(
            query
        )

        hotels = []

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            hotel_lat = item.get(
                "lat",
                item.get("center", {}).get("lat")
            )

            hotel_lon = item.get(
                "lon",
                item.get("center", {}).get("lon")
            )

            hotels.append({
    "name": tags.get(
        "name",
        "Unnamed Hotel"
    ),
    "type": tags.get(
        "tourism",
        "Hotel"
    ),
    "lat": hotel_lat,
    "lon": hotel_lon,
    "image": "https://via.placeholder.com/300x200?text=Hotel",
    "map_link": OSMService.generate_map_link(
        hotel_lat,
        hotel_lon
    )
})

        return hotels[:10]

    @staticmethod
    def get_restaurants(destination):

        coordinates = OSMService.get_coordinates(
            destination
        )

        if not coordinates:
            return []

        lat = coordinates["lat"]
        lon = coordinates["lon"]

        query = f"""
        [out:json];
        (
          node["amenity"~"restaurant|cafe|fast_food|food_court"](around:15000,{lat},{lon});
          way["amenity"~"restaurant|cafe|fast_food|food_court"](around:15000,{lat},{lon});
          relation["amenity"~"restaurant|cafe|fast_food|food_court"](around:15000,{lat},{lon});
        );
        out center;
        """

        data = OSMService._execute_overpass_query(
            query
        )

        restaurants = []

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            rest_lat = item.get(
                "lat",
                item.get("center", {}).get("lat")
            )

            rest_lon = item.get(
                "lon",
                item.get("center", {}).get("lon")
            )

            restaurants.append({
    "name": tags.get(
        "name",
        "Unnamed Restaurant"
    ),
    "type": tags.get(
        "amenity",
        "Restaurant"
    ),
    "cuisine": tags.get(
        "cuisine",
        "Not Specified"
    ),
    "lat": rest_lat,
    "lon": rest_lon,
    "image": "https://via.placeholder.com/300x200?text=Hotel",
    "map_link": OSMService.generate_map_link(
        rest_lat,
        rest_lon
    )
})

        return restaurants[:10]

    @staticmethod
    def get_attractions(destination):

        coordinates = OSMService.get_coordinates(
            destination
        )

        if not coordinates:
            return []

        lat = coordinates["lat"]
        lon = coordinates["lon"]

        query = f"""
        [out:json];
        (
          node["tourism"](around:20000,{lat},{lon});
          way["tourism"](around:20000,{lat},{lon});
          relation["tourism"](around:20000,{lat},{lon});
        );
        out center;
        """

        data = OSMService._execute_overpass_query(
            query
        )

        attractions = []

        allowed_types = [
            "attraction",
            "museum",
            "viewpoint",
            "theme_park",
            "zoo",
            "gallery"
        ]

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            tourism_type = tags.get(
                "tourism",
                ""
            )

            if tourism_type not in allowed_types:
                continue

            attr_lat = item.get(
                "lat",
                item.get("center", {}).get("lat")
            )

            attr_lon = item.get(
                "lon",
                item.get("center", {}).get("lon")
            )

            attraction_name = tags.get(
                "name",
                "Unnamed Attraction"
            )

            image_url = (
                WikipediaService.get_image(
                    f"{attraction_name} {destination}"
                )
            )

            print(
                attraction_name,
                image_url
            )

            attractions.append({

                "name": attraction_name,

                "type": tourism_type,

                "lat": attr_lat,

                "lon": attr_lon,

                "image": image_url,

                "map_link": OSMService.generate_map_link(
                    attr_lat,
                    attr_lon
                )
            })

        return attractions[:10]