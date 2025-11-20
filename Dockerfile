FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create staticfiles directory (skip collectstatic for now)
RUN mkdir -p staticfiles
# RUN python manage.py collectstatic --noinput  # Commented out temporarily

EXPOSE 8000

# Create superuser and start server
CMD sh -c "python manage.py migrate && echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')\" | python manage.py shell && gunicorn project.wsgi:application --bind 0.0.0.0:8000"
