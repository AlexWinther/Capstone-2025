# Use an official Python runtime as a parent image
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install PostgreSQL client tools (psql + pg_isready)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# App default environment (overridable at `docker run`)
ENV DB_HOST=db \
    DB_PORT=5432 \
    DB_NAME=papers \
    DB_USER=user \
    DB_PASSWORD=password \
    CHROMA_HOST=chromadb \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    FLASK_DEBUG=0

# Set the working directory in the container
WORKDIR /app

# Copy project files
COPY . .

# Install only production dependencies
RUN uv sync --locked --no-dev

# Add entrypoint and make it executable
RUN chmod +x /app/docker-entrypoint.sh

# Healthcheck (optional): verifies DB and simple tcp check
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD pg_isready -h "$DB_HOST" -p "$DB_PORT" || exit 1

# Expose the app port (map with -p on run)
EXPOSE 80

# Use entrypoint to wait for DB, run init.sql, then start app
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Fallback CMD (not used because entrypoint execs the app)
CMD ["uv", "run", "app.py", "--no-dev"]
