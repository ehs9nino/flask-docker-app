# Use the official Python image from DockerHub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Flask
RUN pip install flask

# Expose port 5000
EXPOSE 8080


# Define the command to run the app
CMD ["python", "app.py"]
