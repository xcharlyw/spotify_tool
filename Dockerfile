# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app code to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "spotify_tool:app"]