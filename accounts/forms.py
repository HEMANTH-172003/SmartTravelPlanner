from django import forms


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=100
    )

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    phone_number = forms.CharField(
        max_length=15
    )

    nationality = forms.CharField(
        max_length=100
    )

    address = forms.CharField(
        widget=forms.Textarea
    )

    profile_photo = forms.ImageField(
        required=False
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data
    
from django import forms

from .models import UserProfile


class UpdateProfileForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:

        model = UserProfile

        fields = [

            "phone_number",

            "nationality",

            "address",

            "profile_photo"
        ]

from django import forms


class ForgotPasswordForm(forms.Form):

    username = forms.CharField(
        max_length=150
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )