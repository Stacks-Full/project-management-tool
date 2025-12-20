# Use a slim Python image for smaller size
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Dependency Installation Stage

# Install System Dependencies for mysqlclient
# Pointers: We use 'libmariadb-dev-compat' and 'gcc' which are more direct 
# replacements for the tools needed by the 'mysqlclient' C-extension.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libmariadb-dev \
        pkg-config \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements files
COPY requirements/base.txt /tmp/requirements/
COPY requirements/dev.txt /tmp/requirements/

# 3. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements/base.txt -r /tmp/requirements/dev.txt

# 4. Copy the actual application code, tests, pyproject.toml
# COPY app/ /app/app
COPY app/ /app/app
COPY tests/ /app/tests
COPY pyproject.toml /app/pyproject.toml

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PYTHONPATH=/app

# Port that FastAPI runs on (standard for uvicorn)
EXPOSE 8000

# Default command to run the application using Uvicorn with auto-reload (development mode).
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# use the start.sh script for sequential running of commands
# TODO: decide on whether to check the db using docker or the start script
# using docker might be slow but the container is sure to be operational
CMD ["sh","/app/start.sh"]
