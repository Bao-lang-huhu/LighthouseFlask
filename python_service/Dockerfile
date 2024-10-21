# Use the official Python image
FROM python:3.11-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y gcc g++ make wget python3-dev build-essential

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install cmdstanpy and build Stan binaries
RUN pip install cmdstanpy && \
    python -c "import cmdstanpy; cmdstanpy.install_cmdstan()"

# Copy the rest of the application code
COPY . /app

# Expose the port your app will run on
EXPOSE 8080

# Use Gunicorn to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
