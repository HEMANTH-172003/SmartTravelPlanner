from django.urls import path

from .views import *

urlpatterns = [
    path('plan-trip/',TripPlannerAPIView.as_view()),
    path("dashboard/",dashboard_view,name="dashboard"),
    path("my-trips/",my_trips_view,name="my_trips"),
    path("trip/<int:trip_id>/",trip_detail_view,name="trip_detail"),
    path("trip/delete/<int:trip_id>/",delete_trip_view,name="delete_trip"),
    path("trip/edit/<int:trip_id>/",edit_trip_view,name="edit_trip"),
    path("trip/favorite/<int:trip_id>/",favorite_trip_view,name="favorite_trip"),
    path("trip/pdf/<int:trip_id>/",download_trip_pdf_view,name="download_trip_pdf"),
    path("recommendations/",recommendation_view,name="recommendations"),
    path("trip/<int:trip_id>/regenerate/",regenerate_trip_plan_view,name="regenerate_trip_plan"),


    path("trip/<int:trip_id>/share/",toggle_share_trip_view,name="toggle_share_trip"),
    path("share/<uuid:share_token>/",public_trip_view,name="public_trip"),

    path("favorites/",favorite_trips_view,name="favorite_trips"),
]