FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Port SvelteKit dev server runs on
EXPOSE 5173

# Command to run the SvelteKit development server
# The port is picked up from the shell environment (or .env via docker-compose)
CMD ["npm", "run", "dev"]
