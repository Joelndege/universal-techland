# core/tasks.py
from core.ai_processor import OSINTProcessor
from alerts.models import Alert, Location
from datetime import datetime

FEEDS = [
    "https://news.google.com/rss/search?q=crime",
    "https://news.google.com/rss/search?q=accident",
]

osint = OSINTProcessor()

def fetch_and_store_osint_alerts():
    raw_items = osint.fetch_news(FEEDS)
    processed_items = osint.process(raw_items)

    for item in processed_items:
        loc_data = item.get("location")
        location = None

        if loc_data:
            location, _ = Location.objects.get_or_create(
                name=loc_data["name"],
                defaults={"lat": loc_data["lat"], "lng": loc_data["lng"]}
            )

        # Avoid duplicates by title+source+date
        if not Alert.objects.filter(title=item["title"], source="osint").exists():
            Alert.objects.create(
                title=item["title"],
                description=item["text"][:200],
                incident_type=item["category"],
                risk_score=item["risk_score"],
                priority=(
                    "critical" if item["risk_score"]>=80 else
                    "high" if item["risk_score"]>=60 else
                    "medium" if item["risk_score"]>=40 else
                    "low"
                ),
                status="active",
                location=location,
                source="osint",
                created_at=datetime.utcnow()
            )
