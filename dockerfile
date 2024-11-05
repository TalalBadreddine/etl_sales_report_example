# Use the official Python image from the Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install netcat for the wait-for-it.sh script
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Copy and set permissions for wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the application with wait-for-it.sh
CMD ["sh", "-c", "./wait-for-it.sh db 5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
