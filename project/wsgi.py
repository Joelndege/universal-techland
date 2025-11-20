"""
WSGI config for TouristAlertSystem project.
Optimized for Render deployment.
"""

import os
import sys

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django application
application = get_wsgi_application()

# Optional: Add any startup code here if needed
# This ensures the app is fully loaded before serving requests
