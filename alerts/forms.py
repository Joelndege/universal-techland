from django import forms
from .models import Alert

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['title', 'description', 'priority', 'severity', 'status', 'location']

class IncidentReportForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Incident Description")
    lat = forms.FloatField(label="Latitude")
    lng = forms.FloatField(label="Longitude")
    name = forms.CharField(max_length=255, required=False, label="Location Name")
