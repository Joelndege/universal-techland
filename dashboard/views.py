from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from datetime import datetime, timedelta
from dateutil.parser import parse
import json
import requests

from alerts.models import Alert
from core.ai_processor import OSINTProcessor

osint_processor = OSINTProcessor()


# ---------------------------
# Geocode helper with caching
# ---------------------------
def geocode_location(name):
    if not name or name.lower() in ["unknown", "none"]:
        return {"lat": None, "lng": None}

    cache_key = f"geocode_{name.lower()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": name, "format": "json"},
            timeout=5
        )
        data = response.json()
        if data:
            result = {"lat": float(data[0]["lat"]), "lng": float(data[0]["lon"])}
            cache.set(cache_key, result, timeout=86400)  # 24h cache
            return result
    except:
        pass

    return {"lat": None, "lng": None}


# ---------------------------
# Map priority score
# ---------------------------
def map_priority(score):
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


# ---------------------------
# Serialize user alerts
# ---------------------------
def serialize_user_alert(alert):
    loc = {"lat": None, "lng": None}
    if alert.location:
        loc = {"lat": alert.location.lat, "lng": alert.location.lng}

    return {
        "title": alert.title,
        "description": alert.description,
        "priority": alert.priority.lower(),
        "status": alert.status.lower(),
        "location_name": alert.location.name if alert.location else "Unknown",
        "lat": loc["lat"],
        "lng": loc["lng"],
        "created_at": alert.created_at,
        "source": alert.user.username if alert.user else "unknown",
        "type": "user"
    }


# ---------------------------
# Serialize OSINT alerts
# ---------------------------
def serialize_osint_alert(item):
    published = parse(item.get("published")) if item.get("published") else datetime.utcnow()
    risk = item.get("risk_score", 0)
    priority = map_priority(risk)
    severity = "critical" if risk >= 80 else "medium" if risk >= 60 else "low"

    loc = item.get("location") or {"lat": None, "lng": None, "name": "Unknown"}
    return {
        "title": item.get("title", "OSINT Alert"),
        "description": (item.get("text")[:100] + "...") if item.get("text") else "",
        "priority": priority,
        "severity": severity,
        "status": "active",
        "location_name": loc.get("name"),
        "lat": loc.get("lat"),
        "lng": loc.get("lng"),
        "created_at": published,
        "source": "osint",
        "type": "osint"
    }


# ---------------------------
# Dashboard view
# ---------------------------
@login_required
def dashboard_view(request):
    # --- Fetch all user alerts ---
    alerts_qs = Alert.objects.select_related("location", "user").order_by("-created_at")
    user_alerts = [serialize_user_alert(a) for a in alerts_qs]

    # --- Stats ---
    total_alerts = alerts_qs.count()
    critical_alerts = alerts_qs.filter(severity="critical").count()
    active_locations = alerts_qs.filter(status="active").values("location").distinct().count()
    system_status = "Operational"

    # --- Status counts ---
    status_counts = {
        "active": alerts_qs.filter(status="active").count(),
        "pending": alerts_qs.filter(status="pending").count(),
        "resolved": alerts_qs.filter(status="resolved").count(),
    }

    # --- Radar points: alerts with coordinates ---
    radar_points = []
    for alert in alerts_qs:
        if alert.location and alert.location.lat is not None and alert.location.lng is not None:
            radar_points.append({
                "lat": alert.location.lat,
                "lng": alert.location.lng,
                "severity": alert.severity,
            })

    # --- Recent alerts (user alerts only for simplicity) ---
    recent_alerts = user_alerts[:10]

    # --- Daily alerts (last 7 days) ---
    today = datetime.utcnow().date()
    daily_alerts = []
    for i in range(7):
        day = today - timedelta(days=i)
        count = alerts_qs.filter(created_at__date=day).count()
        daily_alerts.append({
            "display_date": day.strftime("%b %d"),
            "count": count
        })
    daily_alerts_json = json.dumps(list(reversed(daily_alerts)))

    # --- Status distribution ---
    statuses = ["active", "pending", "resolved"]
    status_distribution = [
        {"status": s.title(), "count": alerts_qs.filter(status=s).count()}
        for s in statuses
    ]
    status_distribution_json = json.dumps(status_distribution)

    # --- OSINT alerts (Africa-filtered, cached 30 min) ---
    from core.utils import get_africa_news
    osint_alerts = cache.get("africa_osint_alerts")
    if not osint_alerts:
        try:
            africa_news = get_africa_news()
            osint_alerts = [serialize_osint_alert(item) for item in africa_news]
            cache.set("africa_osint_alerts", osint_alerts, timeout=1800)
        except Exception as e:
            print(f"[AFRICA OSINT ERROR] {e}")
            osint_alerts = []

    # --- Combine alerts ---
    all_alerts = user_alerts + osint_alerts
    all_alerts_sorted = sorted(all_alerts, key=lambda x: x["created_at"], reverse=True)

    # --- Prepare for template ---
    recent_activity = all_alerts_sorted[:5]

    # ISO format for JS
    for alert in all_alerts_sorted:
        alert["created_at_iso"] = alert["created_at"].isoformat()

    all_alerts_json = json.dumps(all_alerts_sorted, default=str)
    radar_points_json = json.dumps(radar_points)

    # --- Send context to template ---
    context = {
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "active_locations": active_locations,
        "system_status": system_status,
        "status_counts": status_counts,
        "recent_alerts": recent_alerts,
        "radar_points": radar_points,
        "radar_points_json": radar_points_json,
        "daily_alerts_json": daily_alerts_json,
        "status_distribution_json": status_distribution_json,
        "all_alerts_json": all_alerts_json,
        "recent_activity": recent_activity,
    }

    return render(request, "dashboard/index.html", context)


# --- AJAX endpoint to refresh OSINT alerts ---
@login_required
def refresh_osint_alerts(request):
    if request.method == "POST":
        # Clear cache and fetch new Africa OSINT alerts
        cache.delete("africa_osint_alerts")
        from core.utils import get_africa_news
        from JsonResponse import JsonResponse
        try:
            africa_news = get_africa_news()
            osint_alerts = [serialize_osint_alert(item) for item in africa_news]
            cache.set("africa_osint_alerts", osint_alerts, timeout=1800)
            return JsonResponse({"status": "success", "alerts": osint_alerts})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})




from django.http import JsonResponse
from django.db import connection

def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "Database connected"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
