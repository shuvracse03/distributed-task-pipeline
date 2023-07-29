from django.contrib import admin
from django.urls import path, include


from .views import *

from .apps import AppConfig



app_name = 'request_app'

urlpatterns = [

    path('api/scrape_site/', ScrapeSite.as_view())
]
