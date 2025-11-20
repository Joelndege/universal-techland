from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alerts.models import Alert

@login_required
def map_view(request):
    # Fetch alerts that have a location
    alerts_queryset = Alert.objects.filter(location__isnull=False)

    # Prepare data with coordinates for the template
    alerts = []
    for alert in alerts_queryset:
        loc = alert.location
        alerts.append({
            'title': alert.title,
            'description': alert.description,
            'priority': alert.priority,
            'status': alert.status,
            'lat': getattr(loc, 'latitude', None),  # Make sure Location model has these fields
            'lng': getattr(loc, 'longitude', None),
        })

    return render(request, 'maps/map.html', {'alerts': alerts})
