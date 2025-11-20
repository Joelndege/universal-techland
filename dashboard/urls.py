from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard-view'),
    path('refresh-osint/', views.refresh_osint_alerts, name='refresh-osint'),
     path('', views.test_db, name='test_db'),
]
