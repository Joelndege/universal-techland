from rest_framework import serializers
from .models import Alert, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'lat', 'lng']

class AlertSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Alert
        fields = ['id', 'title', 'description', 'incident_type', 'risk_score',
                  'priority', 'severity', 'status', 'location', 'source', 'created_at']
