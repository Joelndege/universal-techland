import feedparser
import re
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
from geopy.geocoders import Nominatim

# Download NLTK data safely
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


# -----------------------------------------------------
#  OSINT Processor (Fully Automated Threat Intelligence)
# -----------------------------------------------------
class OSINTProcessor:
    """Advanced OSINT + NLP processor for automated alerts."""

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.geolocator = Nominatim(user_agent="tourist-alert-system")

    # -------------------- RSS Fetching --------------------
    def fetch_news(self, feed_urls):
        """Fetch RSS feeds and return raw entries."""
        raw_items = []
        for url in feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:15]:  # more items
                    raw_items.append({
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", ""),
                        "published": entry.get("published", ""),
                        "link": entry.get("link", ""),
                        "source": url
                    })
            except Exception:
                continue
        return raw_items

    # -------------------- Text Cleaning --------------------
    def clean_text(self, text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # -------------------- NLP Classification --------------------
    def classify(self, text):
        """Classify threat level + category from text."""
        clean = text.lower()
        sentiment = self.sia.polarity_scores(clean)['compound']

        # Category detection
        if any(w in clean for w in ["explosion", "bomb", "attack", "terror"]):
            category = "terror"
        elif any(w in clean for w in ["shooting", "gunfire"]):
            category = "shooting"
        elif any(w in clean for w in ["protest", "demonstration", "riot"]):
            category = "unrest"
        elif any(w in clean for w in ["flood", "storm", "earthquake"]):
            category = "disaster"
        elif any(w in clean for w in ["robbery", "crime", "theft"]):
            category = "crime"
        else:
            category = "general"

        # Risk calculation
        base = random.randint(40, 60)

        if category in ["terror", "shooting"]:
            base += 30
        if sentiment < -0.3:
            base += 10

        risk = min(100, base)

        return {
            "risk_score": risk,
            "category": category,
            "sentiment": sentiment
        }

    # -------------------- Location Extraction --------------------
    def extract_location(self, text):
        """Extract city/country from text using regex + geopy."""
        # Simple location detection
        patterns = [
            r"in ([A-Z][a-zA-Z]+)",
            r"at ([A-Z][a-zA-Z]+)",
            r"near ([A-Z][a-zA-Z]+)"
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                place = m.group(1)
                try:
                    loc = self.geolocator.geocode(place)
                    if loc:
                        return {
                            "name": place,
                            "lat": loc.latitude,
                            "lng": loc.longitude
                        }
                except:
                    pass
        return None

    # -------------------- OSINT Processing Pipeline --------------------
    def process(self, items):
        """Convert raw RSS items into structured AI alerts."""
        processed = []

        for item in items:
            text = self.clean_text(item["title"] + " " + item["summary"])

            cls = self.classify(text)
            loc = self.extract_location(text)

            processed.append({
                "title": item["title"],
                "text": text,
                "source": item["source"],
                "published": item["published"],
                "category": cls["category"],
                "risk_score": cls["risk_score"],
                "location": loc,
                "sentiment": cls["sentiment"],
                "type": "osint"
            })

        return processed


# -----------------------------------------------------
#  Incident Processor (User Messages AI)
# -----------------------------------------------------
class IncidentProcessor:
    """NLP processor for user submitted reports."""

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def process_incident(self, text, location):
        clean = text.lower()
        sentiment = self.sia.polarity_scores(clean)['compound']

        if any(w in clean for w in ["robbery", "theft", "crime"]):
            category = "crime"
        elif any(w in clean for w in ["protest", "riot"]):
            category = "unrest"
        elif any(w in clean for w in ["accident", "crash"]):
            category = "accident"
        else:
            category = "general"

        base = random.randint(40, 80)
        if sentiment < -0.4:
            base += 10
        risk = min(100, base)

        return {
            "type": "user",
            "text": text,
            "location": location,
            "category": category,
            "risk_score": risk,
            "sentiment": sentiment,
        }
