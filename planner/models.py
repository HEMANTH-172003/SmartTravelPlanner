from django.db import models
from django.contrib.auth.models import User
import uuid


class Trip(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trips",
        null=True,
        blank=True
    )

    share_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    is_public = models.BooleanField(
        default=False
    )

    source = models.CharField(
        max_length=100
    )

    is_favorite = models.BooleanField(
        default=False
    )

    destination = models.CharField(
        max_length=100
    )

    start_date = models.DateField()

    end_date = models.DateField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    travelers = models.IntegerField()

    TRAVEL_TYPES = (
        ('solo', 'Solo'),
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('couple', 'Couple'),
    )

    travel_type = models.CharField(
        max_length=20,
        choices=TRAVEL_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.source} -> "
            f"{self.destination}"
        )


class TripPlan(models.Model):

    trip = models.OneToOneField(
        Trip,
        on_delete=models.CASCADE,
        related_name="plan"
    )

    budget_allocation = models.JSONField()

    transport = models.JSONField()

    hotels = models.JSONField()

    restaurants = models.JSONField()

    attractions = models.JSONField()

    itinerary = models.JSONField()

    estimated_cost = models.FloatField()

    remaining_budget = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Plan - "
            f"{self.trip.destination}"
        )