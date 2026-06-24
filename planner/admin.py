from django.contrib import admin

from .models import (
    Trip,
    TripPlan
)


admin.site.register(Trip)

admin.site.register(TripPlan)