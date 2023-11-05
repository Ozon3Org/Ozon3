# Use an official Python runtime as a parent image
FROM python:3.8
MAINTAINER label="Rohan Rustagi"
# Set the working directory in the container
WORKDIR /app

# Copy your Python script into the container
COPY *.py .

# Install the required dependencies (in this case, the ozon3 library)
RUN pip install ozon3

# Define the command to run your Python script
CMD ["python", "myapi.py"]
