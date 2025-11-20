from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def update_location(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        if lat and lng:
            request.user.location = Point(float(lng), float(lat))
            request.user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def update_device_token(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if token:
            request.user.device_token = token
            request.user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
