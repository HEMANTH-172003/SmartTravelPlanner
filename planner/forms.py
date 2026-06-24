from django import forms

from .models import Trip


class TripForm(forms.ModelForm):

    class Meta:

        model = Trip

        fields = [

            "source",

            "destination",

            "start_date",

            "end_date",

            "budget",

            "travelers",

            "travel_type"
        ]

        widgets = {

            "start_date":
            forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date":
            forms.DateInput(
                attrs={
                    "type": "date"
                }
            )
        }