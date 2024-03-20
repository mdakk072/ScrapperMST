# Base image
FROM python:3.8-slim

# Install dependencies
RUN apt-get update && apt-get install -y nginx supervisor && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy application code and other files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up Gunicorn
RUN chmod +x ./start-gunicorn.sh

# Set up NGINX
COPY nginx.conf /etc/nginx/sites-available/default
# Remove the existing default configuration, then link your custom configuration
RUN rm -f /etc/nginx/sites-enabled/default && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled

# Set up Supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 80 for NGINX
EXPOSE 80

# Run Supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
