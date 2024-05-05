# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port that the application runs on
EXPOSE $PORT

# Command to run the application
CMD exec gunicorn -b :$PORT -w 4 main:app
