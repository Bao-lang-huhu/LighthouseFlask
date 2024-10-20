# Use the official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt from the python_service directory
COPY python_service/requirements.txt ./

# Upgrade pip and install dependencies
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code from python_service
COPY python_service/ .

# Expose the port your app will run on
EXPOSE 5000

# Command to run your app
CMD ["python", "app.py"]
