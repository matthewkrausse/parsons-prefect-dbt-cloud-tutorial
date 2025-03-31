# Use an official Python runtime as the base image
FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Install git and build dependencies
RUN apt-get update && apt-get install -y git build-essential && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml .
# Copy lockfile if you have one
COPY pyproject.lock* .

# Install dependencies with uv
RUN uv pip install --system --no-cache-dir .

# Runtime stage
FROM python:3.12-slim-bookworm AS runtime

# Copy uv from builder stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code
COPY . .

ARG ENVIRONMENT=dev
ENV ENVIRONMENT=${ENVIRONMENT}

RUN echo "Building image for environment: ${ENVIRONMENT}"
