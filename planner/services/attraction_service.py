from .osm_service import OSMService
from .image_service import ImageService
import random


class AttractionService:

    @staticmethod
    def generate_map_link(lat, lon):

        return (
            f"https://www.google.com/maps/search/"
            f"?api=1&query={lat},{lon}"
        )

    @staticmethod
    def recommend_attractions(
        destination,
        tourism_budget,
        travelers
    ):

        attractions = (
            OSMService.get_attractions(
                destination
            )
        )

        recommendations = []

        for attraction in attractions:

            attraction["image"] = (
    ImageService.get_image(
        attraction["name"]
    )
)

            entry_fee = random.randint(
                0,
                500
            )

            visit_cost = (
                entry_fee * travelers
            )

            if visit_cost <= tourism_budget:

                lat = attraction.get("lat")
                lon = attraction.get("lon")

                recommendations.append({

                    "name": attraction.get(
                        "name",
                        "Unknown Attraction"
                    ),

                    "entry_fee": entry_fee,

                    "rating": round(
                        random.uniform(
                            3.5,
                            5.0
                        ),
                        1
                    ),

                    "visit_cost": visit_cost,

                    "map_link": (
                        AttractionService.generate_map_link(
                            lat,
                            lon
                        )
                        if lat and lon
                        else None
                    )
                })

        recommendations.sort(
            key=lambda x: x["rating"],
            reverse=True
        )

        return recommendations