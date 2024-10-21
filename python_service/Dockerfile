# Use the official Python image
FROM python:3.11-slim

# Install necessary dependencies for Prophet and CmdStanPy
RUN apt-get update && \
    apt-get install -y gcc g++ make wget curl build-essential python3-dev && \
    apt-get install -y libgomp1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -m cmdstanpy.install_cmdstan --dir /opt/cmdstan --overwrite

# Set environment variable for CmdStan path
ENV CMDSTAN=/opt/cmdstan/cmdstan

# Copy the rest of the application code
COPY . /app

# Expose the port your app will run on
EXPOSE 8080

# Use Gunicorn to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
