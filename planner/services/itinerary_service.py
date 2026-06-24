class ItineraryService:

    @staticmethod
    def generate_itinerary(
        trip,
        hotels,
        restaurants,
        attractions
    ):

        days = (
            trip.end_date -
            trip.start_date
        ).days

        itinerary = {}

        attraction_index = 0

        for day in range(1, days + 1):

            day_plan = []

            if day == 1 and hotels:

                day_plan.append(
                    f"Check-in at {hotels[0]['name']}"
                )

            if attraction_index < len(attractions):

                day_plan.append(
                    f"Visit {attractions[attraction_index]['name']}"
                )

                attraction_index += 1

            if restaurants:

                day_plan.append(
                    f"Dine at {restaurants[0]['name']}"
                )

            itinerary[f"Day {day}"] = day_plan

        return itinerary