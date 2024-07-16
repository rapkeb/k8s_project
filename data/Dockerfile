# Use Python 3 as base image
FROM python:3

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python script and CSV file into the container
COPY load.py /app/mongo_loader.py
COPY churn.csv /app/churn.csv

# Install pymongo
RUN pip install pymongo

# Run the Python script to load data and create indexes
CMD ["python", "mongo_loader.py"]
