# ... after your python installation lines ...

# Switch to the root user to manage groups and users
USER root

# vvvvvv ADD THIS ENTIRE BLOCK vvvvvv
# Add a marker so we can prove this new image is running
RUN echo ">>> This is the NEW Jenkins image with Docker permissions v2 <<<"

# The permissions fix
RUN DOCKER_SOCKET_GID=$(stat -c '%g' /var/run/docker.sock) && \
    groupadd -g ${DOCKER_SOCKET_GID} docker && \
    usermod -aG docker jenkins
# ^^^^^^ END OF BLOCK TO ADD ^^^^^^

# Switch back to the standard, non-root 'jenkins' user for security
USER jenkins

# ... the rest of your Dockerfile continues here

# ... the rest of your Dockerfile continues here
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