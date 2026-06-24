class BudgetService:

    @staticmethod
    def allocate_budget(total_budget):

        total_budget = float(total_budget)

        return {
            "transport": total_budget * 0.30,
            "hotel": total_budget * 0.40,
            "food": total_budget * 0.15,
            "tourism": total_budget * 0.15
        }