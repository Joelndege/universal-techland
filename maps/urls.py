# maps/urls.py
from django.urls import path
from . import views

app_name = 'maps'  # THIS IS CRUCIAL

urlpatterns = [
    path('', views.map_view, name='map-view'),
]
