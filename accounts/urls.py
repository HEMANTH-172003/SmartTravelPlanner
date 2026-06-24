from django.urls import path

from .views import *

urlpatterns = [

    path("register/",register_view,name="register"),

    path("login/",login_view,name="login"),

    path("logout/",logout_view,name="logout"),

    path("profile/",profile_view,name="profile"),

    # path("dashboard/",dashboard_view,name="dashboard"),
    path("update-profile/",update_profile_view,name="update_profile"),

    path("change-password/",change_password_view,name="change_password"),

    path("forgot-password/",forgot_password_view,name="forgot_password"),
]