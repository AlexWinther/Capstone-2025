# Use an official Python runtime as a parent image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install PostgreSQL client tools (psql + pg_isready)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . .

# only production dependencies are typically installed.
RUN uv sync --locked --no-dev

# app.py runs on port 5000 (Flask default port)
EXPOSE 3000

# Run app.py when the container launches
CMD ["uv", "run", "app.py"]
