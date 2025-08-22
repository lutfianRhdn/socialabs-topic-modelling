# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1



# Install system dependencies including procps for pgrep command
RUN apt-get update && apt-get install -y \
    procps \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
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

ENV APP_ENV="local"
ENV APP_DEBUG="True"
ENV APP_PORT="6000"
ENV DB_URL_DATAGATHERING="mongodb+srv://application:skripsi@socialabs.pjkgs8t.mongodb.net/"
ENV DB_URL="mongodb+srv://application:skripsi@socialabs.pjkgs8t.mongodb.net/"
ENV DB_NAME="tweets"
ENV AZURE_OPENAI_KEY="6YwpSUX7CKAhTAWRFieW7zj7Q3OoXJNtjGOCsvZsFnTN7g7MyX7SJQQJ99BGACYeBjFXJ3w3AAABACOGG9Qs"
ENV AZURE_OPENAI_ENDPOINT="https://research-etm.openai.azure.com/"
ENV AZURE_OPENAI_MODEL_NAME="gpt-35-turbo"
ENV RABBITMQ_URL="amqp://socialabs:codelabs@57.155.68.154:5672/socialabs-old"

# Copy the Gunicorn configuration file
COPY gunicorn_config.py gunicorn_config.py

# Copy the start_services.py script and make it executable
COPY start_services.py start_services.py
RUN chmod +x start_services.py

# Command to run the start_services.py script
CMD ["python", "start_services.py"]
