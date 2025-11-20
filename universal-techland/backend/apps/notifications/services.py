import firebase_admin
from firebase_admin import messaging
from django.conf import settings
from .models import Notification


def send_fcm_notification(title, body, data=None, tokens=None):
    """
    Send FCM notification to specified tokens or all users with device tokens.
    """
    try:
        # Initialize Firebase if not already done
        if not firebase_admin._apps:
            cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)

        if tokens is None:
            # Get all device tokens from users
            from apps.users.models import User
            tokens = list(User.objects.exclude(device_token__isnull=True).values_list('device_token', flat=True))

        if not tokens:
            return

        # Create message
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=tokens,
        )

        # Send message
        response = messaging.send_multicast(message)
        print(f'Successfully sent message: {response.success_count} success, {response.failure_count} failure')

        return response

    except Exception as e:
        print(f'Error sending FCM notification: {e}')
        return None


def create_notification(user, title, message, notification_type='incident'):
    """
    Create a notification for a user.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )
    return notification
