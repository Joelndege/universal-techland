from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


class Incident(models.Model):
    CATEGORY_CHOICES = [
        ('crime', 'Crime'),
        ('accident', 'Accident'),
        ('weather', 'Weather'),
        ('disaster', 'Disaster'),
        ('civil_unrest', 'Civil Unrest'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    severity = models.IntegerField(default=1)  # 1-5 scale
    location = gis_models.PointField(null=True, blank=True, srid=4326)
    source = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
