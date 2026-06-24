from planner.models import Trip

from planner.ml.recommendation_model import (
    DestinationRecommendationModel
)


class PersonalizedRecommendationService:

    @staticmethod
    def recommend(
        user,
        budget,
        travel_type
    ):

        model = (
            DestinationRecommendationModel()
        )

        recommendations = (
            model.recommend(
                budget,
                travel_type
            )
        )

        visited = [

            trip.destination

            for trip in Trip.objects.filter(
                user=user
            )
        ]

        results = []

        score = 100

        for destination in recommendations:

            if destination in visited:
                continue

            results.append({

                "destination": destination,

                "score": score
            })

            score -= 10

        return results