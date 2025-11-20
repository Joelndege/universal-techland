from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('update-location/', views.update_location, name='update_location'),
    path('update-device-token/', views.update_device_token, name='update_device_token'),
]
