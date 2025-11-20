from celery import shared_task
from .ml_processor import classify_incident
from apps.incidents.models import Incident
from apps.notifications.services import send_fcm_notification
import feedparser
import requests
from datetime import datetime


@shared_task
def fetch_incidents():
    # RSS feeds and APIs to fetch incidents from
    sources = [
        'https://feeds.bbci.co.uk/news/rss.xml',
        'https://rss.cnn.com/rss/edition_world.rss',
        # Add more sources as needed
    ]
    
    for source in sources:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries:
                title = entry.title
                description = getattr(entry, 'description', '')
                category, severity = classify_incident(title + ' ' + description)
                
                # Create incident if it doesn't exist
                incident, created = Incident.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'category': category,
                        'severity': severity,
                        'source': source,
                    }
                )
                
                if created and severity >= 3:  # High severity
                    send_fcm_notification.delay(
                        title="High Alert",
                        body=f"New {category} incident: {title}",
                        data={'incident_id': incident.id}
                    )
        except Exception as e:
            print(f"Error fetching from {source}: {e}")


@shared_task
def analyze_incident_text(incident_id):
    try:
        incident = Incident.objects.get(id=incident_id)
        category, severity = classify_incident(incident.title + ' ' + incident.description)
        incident.category = category
        incident.severity = severity
        incident.save()
    except Incident.DoesNotExist:
        pass


@shared_task
def send_fcm_notification_task(title, body, data=None):
    from apps.notifications.services import send_fcm_notification
    send_fcm_notification(title, body, data)
