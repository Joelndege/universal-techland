"""
ASGI config for TouristAlertSystem project.
Optimized for Render deployment.
"""

import os
import sys

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Import Django ASGI application
from django.core.asgi import get_asgi_application

# Initialize Django application
application = get_asgi_application()

# Optional: Add any async startup code here if needed
