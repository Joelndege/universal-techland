from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Incident
from .serializers import IncidentSerializer


@login_required
def incident_list(request):
    incidents = Incident.objects.all()
    return render(request, 'incidents/incident_list.html', {'incidents': incidents})


@login_required
def incident_detail(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    return render(request, 'incidents/incident_detail.html', {'incident': incident})


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
