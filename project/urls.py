from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirect root to dashboard
    path('', lambda request: redirect('dashboard:dashboard-view')),  

    path('admin/', admin.site.urls),

    # Application routes
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('maps/', include('maps.urls')),
    path('alerts/', include('alerts.urls')),
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('settings/', include('settings.urls')),   # ADDED
    path('forum/', include('forum.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
     path('test-db/', include('dashboard.urls')),
]
