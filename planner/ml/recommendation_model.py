import pandas as pd


class DestinationRecommendationModel:

    def __init__(self):

        self.df = pd.read_csv(
            "planner/ml/destinations.csv"
        )

    def get_budget_category(
        self,
        budget
    ):

        if budget < 20000:
            return "low"

        elif budget < 50000:
            return "medium"

        return "high"

    def recommend(
        self,
        budget,
        travel_type
    ):

        budget_type = (
            self.get_budget_category(
                budget
            )
        )

        recommendations = self.df[

            (self.df["budget_type"] == budget_type)

            &

            (self.df["travel_type"] == travel_type)
        ]

        return recommendations[
            "destination"
        ].tolist()