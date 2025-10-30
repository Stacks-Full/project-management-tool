#!/bin/bash
# start.sh

# The 'db' here MUST match the service name in docker-compose.yml (Step 4)
DB_HOST="db" 
DB_PORT="3306"
TIMEOUT=30

echo "Waiting for $DB_HOST:$DB_PORT to be ready..."

for i in $(seq $TIMEOUT); do
    # Use netcat (nc) to check if the port is open
    if nc -z $DB_HOST $DB_PORT; then
        echo "MySQL is ready! Starting FastAPI..."
        # Execute the application's startup command
        # Assuming main.py is in backend/app/main.py
        exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
        exit 0
    fi
    sleep 1
done

echo "Error: MySQL not ready after $TIMEOUT seconds. Exiting."
exit 1
