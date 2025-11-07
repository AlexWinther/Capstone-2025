#!/usr/bin/env sh
set -euo pipefail

# Default envs (can be overridden at runtime)
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${DB_NAME:=papers}"
: "${DB_USER:=user}"
: "${DB_PASSWORD:=password}"
: "${CHROMA_HOST:=chromadb}"
: "${FLASK_APP:=app.py}"
: "${FLASK_ENV:=production}"
: "${FLASK_DEBUG:=0}"

export PGPASSWORD="${DB_PASSWORD}"

wait_for_db() {
  echo "Waiting for PostgreSQL ${DB_HOST}:${DB_PORT} ..."
  until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" > /dev/null 2>&1; do
    sleep 2
  done
  echo "PostgreSQL is ready."
}

run_init_sql() {
  if [ -f /app/init.sql ]; then
    echo "Running database initialization script ..."
    psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" -f /app/init.sql || true
    echo "Initialization complete."
  else
    echo "No init.sql found, skipping initialization."
  fi
}

main() {
  wait_for_db
  run_init_sql
  echo "Starting application ..."
  exec uv run app.py --no-dev
}

main "$@"
