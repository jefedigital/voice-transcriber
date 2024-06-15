# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set environment variables to reduce output noise.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app
WORKDIR /app

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
#