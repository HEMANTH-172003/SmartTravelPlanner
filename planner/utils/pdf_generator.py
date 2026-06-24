from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_trip_pdf(
    response,
    trip,
    plan
):

    doc = SimpleDocTemplate(
        response
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Smart Travel Planner",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Trip Summary",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Source: {trip.source}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Destination: {trip.destination}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Budget: ₹{trip.budget}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Travelers: {trip.travelers}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Travel Type: {trip.travel_type}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        PageBreak()
    )

    content.append(
        Paragraph(
            "Hotels",
            styles["Heading1"]
        )
    )

    for hotel in plan.hotels:

        content.append(
            Paragraph(
                str(hotel),
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Restaurants",
            styles["Heading1"]
        )
    )

    for restaurant in plan.restaurants:

        content.append(
            Paragraph(
                str(restaurant),
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            "Attractions",
            styles["Heading1"]
        )
    )

    for attraction in plan.attractions:

        content.append(
            Paragraph(
                str(attraction),
                styles["Normal"]
            )
        )

    content.append(
        PageBreak()
    )

    content.append(
        Paragraph(
            "Budget Summary",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Estimated Cost: ₹{plan.estimated_cost}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Remaining Budget: ₹{plan.remaining_budget}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            "Itinerary",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            str(plan.itinerary),
            styles["Normal"]
        )
    )

    doc.build(
        content
    )