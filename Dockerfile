# Use official Python image as base
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=EcomProject.settings

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Run Django migrations and start the server
# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectatatic --noinput"]

