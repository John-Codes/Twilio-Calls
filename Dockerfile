# Use Python as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the Flask app
EXPOSE 5000

# Set environment variables (will be overridden by Back4App or docker-compose if needed)
ENV FLASK_APP=incoming_call_router.py
ENV FLASK_ENV=production

# Command to run the Flask app with a WSGI server for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "incoming_call_router:app"]
