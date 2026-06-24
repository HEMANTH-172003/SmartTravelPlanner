from .osm_service import OSMService
from .image_service import ImageService


class HotelService:

    @staticmethod
    def recommend_hotels(
        destination,
        hotel_budget,
        nights
    ):

        hotels = OSMService.get_hotels(
            destination
        )

        affordable_hotels = []

        for hotel in hotels:

            hotel["image"] = (
    ImageService.get_image(
        hotel["name"]
    )
)

            price_per_night = hotel.get(
                "price_per_night",
                2000
            )

            total_cost = (
                price_per_night * nights
            )

            if total_cost <= hotel_budget:

                hotel["total_cost"] = total_cost

                affordable_hotels.append(
                    hotel
                )

        affordable_hotels.sort(
            key=lambda x: x.get(
                "rating",
                0
            ),
            reverse=True
        )

        return affordable_hotels