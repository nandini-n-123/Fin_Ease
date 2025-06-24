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
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:$PORT", "main:app"]