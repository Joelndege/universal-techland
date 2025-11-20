from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class User(AbstractUser):
    location = models.PointField(null=True, blank=True, srid=4326)
    device_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
