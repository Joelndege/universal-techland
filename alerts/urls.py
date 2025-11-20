from django.urls import path
from .views import IncidentReportView, AlertListAPI, incident_report_page, incident_report_form

app_name = 'alerts'

urlpatterns = [
    # Default page
    path('', incident_report_page, name='incident-home'),

    # API endpoints
    path('api/report/', IncidentReportView.as_view(), name='incident-report-api'),
    path('api/list/', AlertListAPI.as_view(), name='alert-list'),

    # HTML pages
    path('report/', incident_report_page, name='incident-report-page'),
    path('report/form/', incident_report_form, name='incident-report-form'),
]
