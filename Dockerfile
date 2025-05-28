# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend /app

# Copy frontend code and build it
COPY frontend /frontend
WORKDIR /frontend
RUN npm config set registry https://registry.npmjs.org/
RUN npm install && npm run build

# Move frontend build to backend static folder
RUN mkdir -p /app/static && cp -r dist/* /app/static/

# Install backend dependencies
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run Flask
CMD ["flask", "run"]