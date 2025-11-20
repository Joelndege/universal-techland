from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MapLocation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(default=1.0, help_text="Radius in kilometers")
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def coordinates(self):
        return f"{self.latitude}, {self.longitude}"