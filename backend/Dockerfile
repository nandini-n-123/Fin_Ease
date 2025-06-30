# ... after your python installation lines ...

# Switch to the root user to manage groups and users
USER root

# This is the key fix:
# It checks the group ID of the mounted docker.sock file,
# creates a 'docker' group with that same ID inside the container,
# and adds the 'jenkins' user to that group.
RUN DOCKER_SOCKET_GID=$(stat -c '%g' /var/run/docker.sock) && \
    groupadd -g ${DOCKER_SOCKET_GID} docker && \
    usermod -aG docker jenkins

# Switch back to the standard, non-root 'jenkins' user for security
USER jenkins
# ^^^^^^ END OF NEW LINES ^^^^^^

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