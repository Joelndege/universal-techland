from django.core.management.base import BaseCommand
from alerts.models import Alert, Location
from users.models import User
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate demo alerts for testing'

    def handle(self, *args, **options):
        # Malawi and nearby countries coordinates
        locations_data = [
            {"name": "Lilongwe, Malawi", "lat": -13.9626, "lng": 33.7741},
            {"name": "Blantyre, Malawi", "lat": -15.7667, "lng": 35.0167},
            {"name": "Mzuzu, Malawi", "lat": -11.4656, "lng": 34.0207},
            {"name": "Zomba, Malawi", "lat": -15.3833, "lng": 35.3333},
            {"name": "Kasungu, Malawi", "lat": -13.0333, "lng": 33.4833},
            {"name": "Mangochi, Malawi", "lat": -14.4781, "lng": 35.2645},
            {"name": "Karonga, Malawi", "lat": -9.9333, "lng": 33.9333},
            {"name": "Salima, Malawi", "lat": -13.7804, "lng": 34.4587},
            {"name": "Nkhotakota, Malawi", "lat": -12.9274, "lng": 34.2961},
            {"name": "Chitipa, Malawi", "lat": -9.7024, "lng": 33.2697},
            {"name": "Rumphi, Malawi", "lat": -10.8029, "lng": 33.8575},
            {"name": "Mchinji, Malawi", "lat": -13.7984, "lng": 32.8802},
            {"name": "Dedza, Malawi", "lat": -14.3779, "lng": 34.3332},
            {"name": "Ntcheu, Malawi", "lat": -14.8202, "lng": 34.6359},
            {"name": "Balaka, Malawi", "lat": -14.9793, "lng": 34.9558},
            {"name": "Nkhata Bay, Malawi", "lat": -11.6066, "lng": 34.2907},
            {"name": "Likoma, Malawi", "lat": -12.0583, "lng": 34.7333},
            {"name": "Mzimba, Malawi", "lat": -11.9000, "lng": 33.6000},
            {"name": "Chiradzulu, Malawi", "lat": -15.6753, "lng": 35.1407},
            {"name": "Thyolo, Malawi", "lat": -16.0678, "lng": 35.1400},
            # Nearby countries
            {"name": "Dar es Salaam, Tanzania", "lat": -6.7924, "lng": 39.2083},
            {"name": "Lusaka, Zambia", "lat": -15.3875, "lng": 28.3228},
            {"name": "Harare, Zimbabwe", "lat": -17.8252, "lng": 31.0335},
            {"name": "Maputo, Mozambique", "lat": -25.8918, "lng": 32.6051},
        ]

        # Sample alert titles and descriptions
        alert_templates = [
            {"title": "Flood Warning", "desc": "Heavy rainfall causing flooding in low-lying areas", "type": "Natural Disaster"},
            {"title": "Road Accident", "desc": "Multiple vehicle collision on main highway", "type": "Traffic Accident"},
            {"title": "Power Outage", "desc": "Electrical grid failure affecting residential areas", "type": "Infrastructure"},
            {"title": "Medical Emergency", "desc": "Hospital overwhelmed with patients", "type": "Health Crisis"},
            {"title": "Security Alert", "desc": "Suspicious activity reported in downtown area", "type": "Security"},
            {"title": "Fire Incident", "desc": "Building fire requiring evacuation", "type": "Fire Emergency"},
            {"title": "Weather Warning", "desc": "Severe thunderstorm approaching", "type": "Weather"},
            {"title": "Disease Outbreak", "desc": "Contagious illness spreading in community", "type": "Health"},
            {"title": "Theft Report", "desc": "Multiple thefts reported in commercial district", "type": "Crime"},
            {"title": "Transportation Strike", "desc": "Public transport workers on strike", "type": "Civil Unrest"},
            {"title": "Water Contamination", "desc": "Water supply contaminated with pollutants", "type": "Environmental"},
            {"title": "Landslide Risk", "desc": "Unstable terrain posing landslide threat", "type": "Geological"},
            {"title": "Terror Alert", "desc": "Elevated threat level in urban areas", "type": "Security"},
            {"title": "Fuel Shortage", "desc": "Fuel stations running out of supplies", "type": "Economic"},
            {"title": "Communication Blackout", "desc": "Mobile network disruption", "type": "Infrastructure"},
        ]

        # Get or create admin user
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Admin user not found, creating demo user'))
            admin_user = User.objects.create_user(
                username='demo_user',
                email='demo@example.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )

        # Create locations if they don't exist
        locations = []
        for loc_data in locations_data:
            loc, created = Location.objects.get_or_create(
                lat=loc_data["lat"],
                lng=loc_data["lng"],
                defaults={"name": loc_data["name"]}
            )
            locations.append(loc)

        # Generate 100 random alerts (increased from 20)
        alerts_created = 0
        for i in range(100):
            # Random location
            location = random.choice(locations)

            # Random alert template
            template = random.choice(alert_templates)

            # Random severity
            severity = random.choice(['low', 'medium', 'critical'])

            # Random status
            status = random.choice(['active', 'pending', 'resolved'])

            # Random priority based on severity
            if severity == 'critical':
                priority = random.choice(['critical', 'high'])
            elif severity == 'medium':
                priority = random.choice(['high', 'medium'])
            else:
                priority = random.choice(['medium', 'low'])

            # Random risk score
            risk_score = random.randint(0, 100)

            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            created_at = datetime.now() - timedelta(days=days_ago)

            # Create alert
            alert = Alert.objects.create(
                title=template["title"],
                description=template["desc"],
                incident_type=template["type"],
                risk_score=risk_score,
                priority=priority,
                severity=severity,
                status=status,
                location=location,
                user=admin_user,
                created_at=created_at
            )

            alerts_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {alerts_created} demo alerts')
        )
