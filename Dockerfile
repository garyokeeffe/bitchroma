# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app
# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the Flask application to use a different port
ENV FLASK_RUN_PORT=8080

# Specify the command to run Gunicorn with the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
