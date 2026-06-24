from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

import json 
from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count

from .services.recommendation_service import (
    RecommendationService
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Trip, TripPlan
from .forms import TripForm
from .serializers import TripSerializer

from .services.trip_planner_service import (
    TripPlannerService
)
from .services.personalized_recommendation_service import (
    PersonalizedRecommendationService
)

from .utils.pdf_generator import (
    generate_trip_pdf
)


class TripPlannerAPIView(APIView):

    def post(self, request):

        serializer = TripSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        trip = serializer.save()

        plan = (
            TripPlannerService.generate_plan(
                trip
            )
        )

        return Response(
            plan,
            status=status.HTTP_200_OK
        )


@login_required
def dashboard_view(request):

    user_trips = Trip.objects.filter(
        user=request.user
    )

    total_trips = user_trips.count()

    favorite_trips = user_trips.filter(
        is_favorite=True
    ).count()

    total_budget = (
    user_trips.aggregate(
        total=Sum("budget")
    )["total"]
    or 0
)

    destinations = (
        user_trips
        .values("destination")
        .distinct()
        .count()
    )

    top_destination = (
        user_trips
        .values("destination")
        .annotate(
            total=Count("destination")
        )
        .order_by("-total")
        .first()
    )

    solo_count = user_trips.filter(
        travel_type="solo"
    ).count()

    family_count = user_trips.filter(
        travel_type="family"
    ).count()

    friends_count = user_trips.filter(
        travel_type="friends"
    ).count()

    couple_count = user_trips.filter(
        travel_type="couple"
    ).count()

    recent_trips = Trip.objects.filter(
    user=request.user
    ).order_by("-id")[:2]

    if request.method == "POST":

        form = TripForm(request.POST)

        if form.is_valid():

            trip = form.save(
                commit=False
            )

            trip.user = request.user

            trip.save()

            result = (
                TripPlannerService.generate_plan(
                    trip
                )
            )

            TripPlan.objects.create(

                trip=trip,

                budget_allocation=result[
                    "budget_allocation"
                ],

                transport=result[
                    "transport"
                ],

                hotels=result[
                    "hotels"
                ],

                restaurants=result[
                    "restaurants"
                ],

                attractions=result[
                    "attractions"
                ],

                itinerary=result[
                    "itinerary"
                ],

                estimated_cost=result[
                    "estimated_cost"
                ],

                remaining_budget=result[
                    "remaining_budget"
                ]
            )

            return render(

                request,

                "planner/result.html",

                {
                    "result": result
                }
            )

    else:

        form = TripForm()

    return render(

        request,

        "planner/dashboard.html",

        {

            "form": form,

            "total_trips": total_trips,

            "favorite_trips": favorite_trips,

            "total_budget": total_budget,

            "destinations": destinations,

            "top_destination": top_destination,

            "solo_count": solo_count,

            "family_count": family_count,

            "friends_count": friends_count,

            "couple_count": couple_count,

            "recent_trips": recent_trips
        }
    )

@login_required
def my_trips_view(request):

    search = request.GET.get(
        "search"
    )

    trips = Trip.objects.filter(
        user=request.user
    )

    if search:

        trips = trips.filter(
            destination__icontains=search
        )

    trips = trips.order_by(
        "-created_at"
    )

    return render(

        request,

        "planner/my_trips.html",

        {
            "trips": trips
        }
    )

@login_required
def trip_detail_view(
    request,
    trip_id
):

    trip = Trip.objects.get(
        id=trip_id,
        user=request.user
    )

    plan = TripPlan.objects.filter(
        trip=trip
    ).first()

    if not plan:

        return render(

            request,

            "planner/no_plan.html",

            {
                "trip": trip
            }
        )
    print(type(plan.attractions))
    print(plan.attractions)

    return render(

        request,

        "planner/trip_detail.html",

        {
            "trip": trip,
            "plan": plan
        }
    )

@login_required
def delete_trip_view(
    request,
    trip_id
):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user
    )

    trip.delete()

    return redirect(
        "my_trips"
    )

@login_required
def edit_trip_view(
    request,
    trip_id
):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user
    )

    if request.method == "POST":

        form = TripForm(
            request.POST,
            instance=trip
        )

        if form.is_valid():

            form.save()

            return redirect(
                "trip_detail",
                trip_id=trip.id
            )

    else:

        form = TripForm(
            instance=trip
        )

    return render(

        request,

        "planner/edit_trip.html",

        {
            "form": form,
            "trip": trip
        }
    )

@login_required
def favorite_trip_view(
    request,
    trip_id
):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user
    )

    trip.is_favorite = (
        not trip.is_favorite
    )

    trip.save()

    return redirect(
        "trip_detail",
        trip_id=trip.id
    )

@login_required
def download_trip_pdf_view(
    request,
    trip_id
):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user
    )

    plan = get_object_or_404(

        TripPlan,

        trip=trip
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="trip_{trip.id}.pdf"'
    )

    generate_trip_pdf(
        response,
        trip,
        plan
    )

    return response

@login_required
def recommendation_view(

    request
):

    recommendations = []

    if request.method == "POST":

        budget = int(
            request.POST.get(
                "budget"
            )
        )

        travel_type = (
            request.POST.get(
                "travel_type"
            )
        )

        recommendations = (
            
            PersonalizedRecommendationService.recommend(

    request.user,

    budget,

    travel_type
)
        )

    return render(

        request,

        "planner/recommendations.html",

        {
            "recommendations":
            recommendations
        }
    )

@login_required
def regenerate_trip_plan_view(
    request,
    trip_id
):

    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user
    )

    result = (
        TripPlannerService.generate_plan(
            trip
        )
    )

    plan, created = (
        TripPlan.objects.get_or_create(
            trip=trip
        )
    )

    plan.budget_allocation = result[
        "budget_allocation"
    ]

    plan.transport = result[
        "transport"
    ]

    plan.hotels = result[
        "hotels"
    ]

    plan.restaurants = result[
        "restaurants"
    ]

    plan.attractions = result[
        "attractions"
    ]

    plan.itinerary = result[
        "itinerary"
    ]

    plan.estimated_cost = result[
        "estimated_cost"
    ]

    plan.remaining_budget = result[
        "remaining_budget"
    ]

    plan.save()

    return redirect(
        "trip_detail",
        trip_id=trip.id
    )

@login_required
def toggle_share_trip_view(
    request,
    trip_id
):

    trip = get_object_or_404(

        Trip,

        id=trip_id,

        user=request.user
    )

    trip.is_public = (
        not trip.is_public
    )

    trip.save()

    return redirect(
        "trip_detail",
        trip_id=trip.id
    )

def public_trip_view(
    request,
    share_token
):

    trip = get_object_or_404(

        Trip,

        share_token=share_token,

        is_public=True
    )

    plan = get_object_or_404(

        TripPlan,

        trip=trip
    )

    return render(

        request,

        "planner/public_trip.html",

        {

            "trip": trip,

            "plan": plan
        }
    )

@login_required
def favorite_trips_view(request):

    trips = Trip.objects.filter(
        user=request.user,
        is_favorite=True
    ).order_by(
        "-created_at"
    )

    total_favorites = trips.count()

    return render(

        request,

        "planner/favorite_trips.html",

        {

            "trips": trips,

            "total_favorites": total_favorites
        }
    )
