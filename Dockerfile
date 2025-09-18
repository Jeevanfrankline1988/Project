# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
