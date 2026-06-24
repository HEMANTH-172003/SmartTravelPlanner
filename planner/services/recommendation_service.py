from planner.ml.recommendation_model import (
    DestinationRecommendationModel
)


class RecommendationService:

    @staticmethod
    def get_recommendations(
        budget,
        travel_type
    ):

        model = (
            DestinationRecommendationModel()
        )

        return model.recommend(
            budget,
            travel_type
        )