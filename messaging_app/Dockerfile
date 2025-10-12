# Use official Python 3.10 slim base image to keep it lightweight
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app code to the container
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
