# Use the official Python image from DockerHub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Flask
RUN pip install flask pymongo 

ENV MONGO_URI "mongodb+srv://ehsanqader9:2vFF04OULmsDK3FM@cluster0.w1skg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Expose port 5000
EXPOSE 8080


# Define the command to run the app
CMD ["python", "app.py"]
