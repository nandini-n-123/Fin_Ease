# Start with your existing FROM line
FROM jenkins/jenkins:lts-jdk17

# vvvvvv ADD THESE FOUR LINES vvvvvv
# Switch to the root user to gain permission to install packages
USER root

# Run the commands to update the package list and install python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Switch back to the standard, non-root 'jenkins' user for security
USER jenkins
# ^^^^^^ END OF NEW LINES ^^^^^^

# ... the rest of your Dockerfile continues here
# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install the packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code into the container
COPY . /code/

# The command to run your app using Gunicorn when the container starts
# This uses the Mangum adapter, which is necessary for AWS Lambda
CMD ["/bin/sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app"]