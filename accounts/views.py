from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth.forms import (
    PasswordChangeForm
)

from django.contrib.auth import (
    update_session_auth_hash
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.models import User

from .forms import (
    RegisterForm,
    UpdateProfileForm,
    ForgotPasswordForm
)

from django.contrib.auth.decorators import (
    login_required
)

from .forms import RegisterForm
from .models import UserProfile


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data["phone_number"],
                nationality=form.cleaned_data["nationality"],
                address=form.cleaned_data["address"],
                profile_photo=form.cleaned_data["profile_photo"]
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("dashboard")

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("login")


@login_required
def profile_view(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile
        }
    )

@login_required
def update_profile_view(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    if request.method == "POST":

        form = UpdateProfileForm(

            request.POST,

            request.FILES,

            instance=profile
        )

        if form.is_valid():

            form.save()

            request.user.email = (
                request.POST.get(
                    "email"
                )
            )

            request.user.save()

            return redirect(
                "profile"
            )

    else:

        form = UpdateProfileForm(
            instance=profile
        )

    return render(

        request,

        "accounts/update_profile.html",

        {
            "form": form,
            "profile": profile
        }
    )


@login_required
def change_password_view(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect(
                "profile"
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(

        request,

        "accounts/change_password.html",

        {
            "form": form
        }
    )

def forgot_password_view(request):

    if request.method == "POST":

        form = ForgotPasswordForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data[
                "username"
            ]

            new_password = form.cleaned_data[
                "new_password"
            ]

            confirm_password = form.cleaned_data[
                "confirm_password"
            ]

            if new_password != confirm_password:

                return render(
                    request,
                    "accounts/forgot_password.html",
                    {
                        "form": form,
                        "error":
                        "Passwords do not match"
                    }
                )

            try:

                user = User.objects.get(
                    username=username
                )

                user.set_password(
                    new_password
                )

                user.save()

                return redirect(
                    "login"
                )

            except User.DoesNotExist:

                return render(
                    request,
                    "accounts/forgot_password.html",
                    {
                        "form": form,
                        "error":
                        "User not found"
                    }
                )

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "accounts/forgot_password.html",
        {
            "form": form
        }
    )