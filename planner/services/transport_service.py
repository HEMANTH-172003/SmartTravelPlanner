class TransportService:

    @staticmethod
    def recommend_transport(source, destination, budget):

        budget = float(budget)

        transport_options = []

        # Bus
        transport_options.append({
            "type": "Bus",
            "name": "Luxury Bus",
            "estimated_cost": 1500
        })

        # Train
        transport_options.append({
            "type": "Train",
            "name": "Express Train",
            "estimated_cost": 2500
        })

        # Flight
        transport_options.append({
            "type": "Flight",
            "name": "Economy Flight",
            "estimated_cost": 6000
        })

        affordable_options = []

        for option in transport_options:

            if option["estimated_cost"] <= budget:
                affordable_options.append(option)

        return affordable_options