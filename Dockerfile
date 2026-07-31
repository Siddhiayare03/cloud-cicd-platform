# Base Image
FROM python:3.13-slim

# Working directory inside container
WORKDIR /app

# Copy dependency list
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ .

# Application port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]