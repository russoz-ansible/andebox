# Use the official Microsoft Python devcontainer image from the Docker Hub
FROM mcr.microsoft.com/devcontainers/python:3

# Set the working directory in the container
WORKDIR /workspace

# Install Poetry
RUN pip install \
    tox \
    pylint \
    flake8
