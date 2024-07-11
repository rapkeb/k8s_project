# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

#Define environment variable
ENV FLASK_APP=app.py

#Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"]
