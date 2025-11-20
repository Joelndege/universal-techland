import requests
from core.ai_processor import OSINTProcessor
from django.core.cache import cache

def get_africa_news():
    """
    Fetch and filter OSINT news to Africa-related alerts.
    """
    # Africa countries list for filtering
    africa_countries = [
        'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon',
        'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Cote d\'Ivoire', 'Djibouti', 'Egypt',
        'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea',
        'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
        'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda',
        'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa',
        'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
    ]

    # Check cache first
    cached_news = cache.get("africa_osint_alerts")
    if cached_news:
        return cached_news

    # Fetch global OSINT feeds
    osint_processor = OSINTProcessor()
    feeds = [
        "https://news.google.com/rss/search?q=crime+africa",
        "https://news.google.com/rss/search?q=accident+africa",
        "https://news.google.com/rss/search?q=terror+africa",
        "https://news.google.com/rss/search?q=disaster+africa"
    ]

    try:
        raw_feed = osint_processor.fetch_news(feeds)
        processed = osint_processor.process(raw_feed)

        # Filter to Africa-related
        africa_news = []
        for item in processed:
            text = item.get("text", "").lower()
            title = item.get("title", "").lower()
            location = item.get("location")

            # Check if any Africa country mentioned
            is_africa = any(country.lower() in text or country.lower() in title for country in africa_countries)

            # Or if location is in Africa (rough check by lat/lng)
            if location and location.get("lat") and location.get("lng"):
                lat, lng = location["lat"], location["lng"]
                if -35 <= lat <= 37 and -25 <= lng <= 55:  # Rough Africa bounds
                    is_africa = True

            if is_africa:
                africa_news.append(item)

        # Cache for 30 minutes
        cache.set("africa_osint_alerts", africa_news, timeout=1800)
        return africa_news

    except Exception as e:
        print(f"[AFRICA NEWS ERROR] {e}")
        return []
