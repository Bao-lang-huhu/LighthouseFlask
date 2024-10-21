# Use the official Python image
FROM python:3.11-slim

# Install necessary dependencies for Prophet, GLIBC, and other tools
RUN apt-get update && \
    apt-get install -y gcc g++ make wget gawk bison && \
    wget https://ftp.gnu.org/gnu/libc/glibc-2.36.tar.gz && \
    tar -xvzf glibc-2.36.tar.gz && \
    cd glibc-2.36 && \
    mkdir build && cd build && \
    ../configure --prefix=/opt/glibc-2.36 && \
    make && make install && \
    rm -rf /glibc-2.36*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port your app will run on
EXPOSE 8080

# Use Gunicorn to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
