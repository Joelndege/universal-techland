# Bind to all network interfaces on port 8000
bind = "0.0.0.0:8000"

# Render free tier only has 512 MB RAM
# Keep workers and threads low to prevent memory issues
workers = 2
threads = 2

# Simple synchronous workers to avoid async memory spikes
worker_class = "sync"

# Maximum request timeout (seconds)
timeout = 120

# Logging level
loglevel = "info"

# Restart workers after handling a number of requests to avoid memory leaks
max_requests = 500
max_requests_jitter = 50

# Optional: graceful timeout for shutdown (seconds)
graceful_timeout = 30
