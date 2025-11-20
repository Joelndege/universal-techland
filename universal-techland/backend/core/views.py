from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from apps.incidents.models import Incident
from apps.notifications.models import Notification
from django.contrib.gis.geos import Point


@login_required
def dashboard(request):
    incidents = Incident.objects.all().order_by('-created_at')[:10]
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'incidents': incidents,
        'notifications': notifications,
    }
    return render(request, 'dashboard.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required
def profile(request):
    if request.method == 'POST':
        # Update location
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        if lat and lng:
            request.user.location = Point(float(lng), float(lat))
            request.user.save()
            messages.success(request, 'Location updated successfully.')
        return redirect('core:profile')
    return render(request, 'profile.html')
