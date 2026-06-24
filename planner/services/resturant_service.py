from .osm_service import OSMService
from .image_service import ImageService


class RestaurantService:

    @staticmethod
    def recommend_restaurants(
        destination,
        food_budget,
        travelers
    ):

        restaurants = (
            OSMService.get_restaurants(
                destination
            )
        )

        affordable_restaurants = []

        for restaurant in restaurants:

            restaurant["image"] = (
    ImageService.get_image(
        restaurant["name"]
    )
)

            avg_cost = restaurant.get(
                "avg_cost_per_person",
                500
            )

            estimated_meal_cost = (
                avg_cost * travelers
            )

            if estimated_meal_cost <= food_budget:

                restaurant[
                    "estimated_meal_cost"
                ] = estimated_meal_cost

                affordable_restaurants.append(
                    restaurant
                )

        affordable_restaurants.sort(
            key=lambda x: x.get(
                "rating",
                0
            ),
            reverse=True
        )

        return affordable_restaurants
    