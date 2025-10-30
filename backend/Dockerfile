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
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements files
COPY requirements/base.txt /tmp/requirements/
COPY requirements/dev.txt /tmp/requirements/

# 3. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements/base.txt -r /tmp/requirements/dev.txt

# 4. Copy the actual application code
COPY app/ /app/app

ENV PYTHONPATH=/app

# Port that FastAPI runs on (standard for uvicorn)
EXPOSE 8000

# Default command to run the application using Uvicorn with auto-reload (development mode).
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
