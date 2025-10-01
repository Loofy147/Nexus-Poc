# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level build dependencies that may be needed by some libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the Spacy language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application's code
COPY . .

# Make port 5003 available
EXPOSE 5003

# Define environment variable
ENV FLASK_APP app.py

# Run the command to start the server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5003"]