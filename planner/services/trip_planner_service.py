import time

from .budget_service import BudgetService
from .transport_service import TransportService
from .hotel_service import HotelService
from .resturant_service import RestaurantService
from .attraction_service import AttractionService
from .itinerary_service import ItineraryService


class TripPlannerService:

    @staticmethod
    def generate_plan(trip):

        budget = BudgetService.allocate_budget(
            trip.budget
        )

        nights = (
            trip.end_date - trip.start_date
        ).days

        transport_data = (
            TransportService.recommend_transport(
                trip.source,
                trip.destination,
                budget["transport"]
            )
        )

        time.sleep(1)

        hotels = (
            HotelService.recommend_hotels(
                trip.destination,
                budget["hotel"],
                nights
            )
        )

        time.sleep(1)

        restaurants = (
            RestaurantService.recommend_restaurants(
                trip.destination,
                budget["food"],
                trip.travelers
            )
        )

        time.sleep(1)

        attractions = (
            AttractionService.recommend_attractions(
                trip.destination,
                budget["tourism"],
                trip.travelers
            )
        )

        itinerary = (
            ItineraryService.generate_itinerary(
                trip,
                hotels,
                restaurants,
                attractions
            )
        )

        transport_cost = 0

        if (
            isinstance(transport_data, dict)
            and transport_data.get("options")
        ):
            transport_cost = min(
                option.get(
                    "estimated_cost",
                    0
                )
                for option in transport_data[
                    "options"
                ]
            )

        hotel_cost = (
            hotels[0].get(
                "total_cost",
                0
            )
            if hotels else 0
        )

        food_cost = sum(
            restaurant.get(
                "estimated_meal_cost",
                0
            )
            for restaurant in restaurants
        )

        tourism_cost = sum(
            attraction.get(
                "visit_cost",
                0
            )
            for attraction in attractions
        )

        estimated_cost = (
            transport_cost
            + hotel_cost
            + food_cost
            + tourism_cost
        )

        remaining_budget = (
            float(trip.budget)
            - estimated_cost
        )

        return {

            "trip_id": trip.id,

            "trip": {

                "source": trip.source,

                "destination": trip.destination,

                "budget": trip.budget,

                "travelers": trip.travelers,

                "travel_type": trip.travel_type,

                "start_date": trip.start_date,

                "end_date": trip.end_date
            },

            "budget_allocation": budget,

            "transport": transport_data,

            "hotels": hotels,

            "restaurants": restaurants,

            "attractions": attractions,

            "itinerary": itinerary,

            "estimated_cost": estimated_cost,

            "remaining_budget": remaining_budget
        }