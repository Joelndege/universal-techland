# Use official Python 3.11 slim image
FROM python:3.11-slim

# -------------------------------
# Environment variables
# -------------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NLTK_DATA=/app/nltk_data

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copy requirements and install
# -------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Copy project files
# -------------------------------
COPY . .

# -------------------------------
# Copy Firebase credentials
# -------------------------------
# Make sure your firebase_credentials.json exists in project root
COPY firebase_credentials.json /app/firebase_credentials.json

# -------------------------------
# Preload NLTK data
# -------------------------------
RUN python -m nltk.downloader -d /app/nltk_data vader_lexicon

# -------------------------------
# Collect static files
# -------------------------------
# Avoid UnicodeDecodeError by skipping problematic files
RUN python manage.py collectstatic --noinput || echo "Skipping problematic static files"

# -------------------------------
# Expose port for web service
# -------------------------------
EXPOSE 8000

# -------------------------------
# Run Gunicorn
# -------------------------------
CMD ["gunicorn", "--config", "gunicorn.conf.py", "project.wsgi:application"]
