from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Alert, Location
from .serializers import AlertSerializer
from core.ai_processor import IncidentProcessor
from notifications.services import NotificationService

from rest_framework.test import APIRequestFactory


# ============================================================
# INCIDENT REPORT API (Authenticated)
# ============================================================
class IncidentReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        text = data.get("text")
        loc_data = data.get("location")

        print(f"DEBUG API: Received data - text: {text}, location: {loc_data}")  # Debug print

        if not text or not loc_data:
            return Response(
                {"error": f"Text and location are required. Received text='{text}', location={loc_data}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        processor = IncidentProcessor()
        incident = processor.process_incident(text, loc_data)

        # Create alert if risk >= threshold (lowered to 50 for testing)
        if incident["risk_score"] >= 50:
            location_obj, _ = Location.objects.get_or_create(
                lat=loc_data["lat"],
                lng=loc_data["lng"],
                defaults={"name": loc_data.get("name", f"Location ({loc_data['lat']}, {loc_data['lng']})")}
            )

            alert_obj = Alert.objects.create(
                title=text[:50] + ("..." if len(text) > 50 else ""),
                description=text,
                incident_type=incident["category"],
                risk_score=incident["risk_score"],
                priority="critical" if incident["risk_score"] >= 80 else "high",
                severity="critical" if incident["risk_score"] >= 80 else "medium",
                status="active",
                location=location_obj,
                user=request.user
            )

            # Send notifications to nearby users
            NotificationService.send_alert(alert_obj)

            serializer = AlertSerializer(alert_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "Incident processed, no alert created (risk score too low)"}, status=status.HTTP_200_OK)


# ============================================================
# PUBLIC ALERT LIST API
# ============================================================
class AlertListAPI(APIView):
    permission_classes = []

    def get(self, request):
        alerts = Alert.objects.all().order_by("-created_at")
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


# ============================================================
# HTML PAGE FOR INCIDENT REPORT
# ============================================================
@login_required
def incident_report_page(request):
    return render(request, "alerts/incident_report.html")


# ============================================================
# FORM PAGE THAT USES API INTERNALLY
# ============================================================
@login_required
def incident_report_form(request):
    message = ""

    if request.method == "POST":
        text = request.POST.get("text")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        name = request.POST.get("name")

        print(f"DEBUG: Received POST data - text: {text}, lat: {lat}, lng: {lng}, name: {name}")  # Debug print

        if not text or not lat or not lng:
            message = f"Please provide text and location. Received: text='{text}', lat='{lat}', lng='{lng}'"
        else:
            try:
                # Convert to float to ensure valid numbers
                lat_float = float(lat)
                lng_float = float(lng)

                data = {
                    "text": text,
                    "location": {"lat": lat_float, "lng": lng_float, "name": name or ""}
                }

                print(f"DEBUG: Sending data to API: {data}")  # Debug print

                factory = APIRequestFactory()
                api_request = factory.post("/alerts/api/report/", data, format="json")
                api_request.user = request.user

                response = IncidentReportView.as_view()(api_request)

                print(f"DEBUG: API Response status: {response.status_code}, data: {response.data}")  # Debug print

                if response.status_code == 201:
                    message = "✅ Incident reported successfully! The alert will appear on the map."
                else:
                    message = f"Error: {response.data.get('error') or response.data.get('message') or str(response.data)}"
            except ValueError as e:
                message = f"Invalid latitude/longitude format: {str(e)}"
            except Exception as e:
                message = f"Error processing report: {str(e)}"

    return render(request, "alerts/incident_report_form.html", {"message": message})
