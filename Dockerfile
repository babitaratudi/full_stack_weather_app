# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install Node.js and npm (for frontend build)
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy and install backend dependencies first (leverage Docker cache)
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy and install frontend dependencies first (leverage Docker cache)
COPY frontend/package.json /frontend/
WORKDIR /frontend
RUN npm config set registry https://registry.npmjs.org/
RUN npm install

# Copy the rest of the backend and frontend code
COPY backend /app
COPY frontend /frontend

# Build frontend
WORKDIR /frontend
RUN npm run build

# Move frontend build to backend static folder
RUN mkdir -p /app/static && cp -r dist/* /app/static/

# Set workdir back to backend
WORKDIR /app

# Expose port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run Flask
CMD ["flask", "run"]