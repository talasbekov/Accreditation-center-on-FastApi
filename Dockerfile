FROM python:3.14.0a1-slim-bookworm

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Install wget
RUN apt-get update && apt-get install libssl-dev wkhtmltopdf -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

# Copy Pipfile and Pipfile.lock
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt
COPY ./api/v1/docs/cities.csv /app/docs/cities.csv

# Copy project
COPY . .