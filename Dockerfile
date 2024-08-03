# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask application will run on
EXPOSE 6000

# Copy the Gunicorn configuration file
COPY gunicorn_config.py gunicorn_config.py

# Copy the start_services.py script and make it executable
COPY start_services.py start_services.py
RUN chmod +x start_services.py

# Command to run the start_services.py script
CMD ["python", "start_services.py"]
