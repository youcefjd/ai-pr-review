FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY autonomous_reviewer/ ./autonomous_reviewer/

# Expose dashboard port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run dashboard by default
CMD ["python", "autonomous_reviewer/dashboard.py"]
