# Copyright (c) 2025, Alexei Znamensky
# All rights reserved.
#
# This file is part of the Andebox project and is distributed under the terms
# of the BSD 3-Clause License. See LICENSE file for details.

# Use the official Microsoft Python devcontainer image from the Docker Hub
FROM mcr.microsoft.com/devcontainers/python:3

# Set the working directory in the container
WORKDIR /workspace

# Install poetry
RUN pip install -U pip \
 && pip install poetry pre-commit tox
