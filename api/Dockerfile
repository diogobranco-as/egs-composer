# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL and ngrok
RUN apt-get update && \
    apt-get install -y gcc libpq-dev wget && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]