# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level build dependencies required by the advanced libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Make port 6000 available
EXPOSE 6000

# Define environment variable
ENV FLASK_APP app.py

# Run the command to start the server
CMD ["flask", "run", "--host=0.0.0.0", "--port=6000"]