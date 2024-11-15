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

ENV APP_ENV=local
ENV APP_DEBUG=True
ENV APP_PORT=6000
ENV DB_URL=mongodb+srv://application:CodeLabs011013@socialabs-database.global.mongocluster.cosmos.azure.com
ENV DB_NAME=tweets
ENV AZURE_OPENAI_KEY=4LpCIE7GP3QfCliKOSyLSu44HWGSJUeMAzcfSqgj8XS5EflenP1sJQQJ99AJACYeBjFXJ3w3AAAAACOG4ECn
ENV AZURE_OPENAI_ENDPOINT=https://socialabs-llm.openai.azure.com/
ENV AZURE_OPENAI_MODEL_NAME=socialabs-gpt-35
ENV RABBITMQ_URL=amqp://application:CodeLabs011013@20.40.101.128:5672

# Copy the Gunicorn configuration file
COPY gunicorn_config.py gunicorn_config.py

# Copy the start_services.py script and make it executable
COPY start_services.py start_services.py
RUN chmod +x start_services.py

# Command to run the start_services.py script
CMD ["python", "start_services.py"]
