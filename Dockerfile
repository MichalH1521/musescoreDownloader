# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary system dependencies (for Selenium)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libfontconfig1 \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


ENV CHROME_BIN=/usr/bin/chromium
# Copy everything, including the existing venv
COPY . .

# Expose port 5000
EXPOSE 5000

# Activate venv and run the Flask app
CMD ["python", "-u", "run.py"]
