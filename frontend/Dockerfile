# Use Node.js 20 slim image for a smaller footprint
FROM node:20-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (Vite's default)
EXPOSE 5173

# Start the application in development mode
# --host 0.0.0.0 is necessary to allow access from outside the container
# We use the FRONTEND_PORT environment variable from .env if provided
CMD ["sh", "-c", "npm run dev -- --host 0.0.0.0 --port ${FRONTEND_PORT:-5173}"]
