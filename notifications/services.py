# notifications/services.py
from pyfcm import FCMNotification
from alerts.models import Alert
from users.models import User  # Assuming each user has 'location' and 'fcm_token'
from geopy.distance import geodesic


class NotificationService:
    """
    Sends push notifications to users within a given radius (km) of an alert.
    Works for both OSINT and manual alerts.
    """
    FCM_API_KEY = "YOUR_FIREBASE_API_KEY"  # Replace with your actual key
    RADIUS_KM = 5  # Notify users within 5 km

    @classmethod
    def send_alert(cls, alert: Alert):
        if not alert.location:
            return  # Cannot send notifications without alert location

        push_service = FCMNotification(api_key=cls.FCM_API_KEY)
        recipients = []

        # Iterate through all users with valid location & FCM token
        for user in User.objects.all():
            if not user.location or not getattr(user, "fcm_token", None):
                continue

            # Compute distance in km
            distance = cls.calculate_distance(user.location, alert.location)
            if distance <= cls.RADIUS_KM:
                recipients.append(user.fcm_token)

        # Send push notification if we have recipients
        if recipients:
            message_title = f"Alert: {alert.incident_type.upper()}"
            message_body = f"{alert.description[:150]} | Risk: {alert.risk_score}"

            try:
                push_service.notify_multiple_devices(
                    registration_ids=recipients,
                    message_title=message_title,
                    message_body=message_body
                )
            except Exception as e:
                print(f"[Notification ERROR] {e}")

    @staticmethod
    def calculate_distance(user_loc, alert_loc):
        """
        Calculate distance in km between two locations.
        user_loc and alert_loc are Django model instances with .lat and .lng
        """
        point1 = (user_loc.lat, user_loc.lng)
        point2 = (alert_loc.lat, alert_loc.lng)
        return geodesic(point1, point2).km
