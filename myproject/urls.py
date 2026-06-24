from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from .views import (
    home_view,
    about_view
)

urlpatterns = [

    path(
        '',
        home_view,
        name='home'
    ),

    path(
        'about/',
        about_view,
        name='about'
    ),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/',
        include('planner.urls')
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)