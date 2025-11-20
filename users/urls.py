from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),        # /users/ → list of all users
    path('profile/', views.profile_view, name='profile'),  # /users/profile/ → logged-in user's profile
]
