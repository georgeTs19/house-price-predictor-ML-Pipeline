# Dockerfile for FastAPI
FROM python:3.11-slim

WORKDIR /app

# Install dependencies for FastAPI
COPY src/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy API code
COPY src/api /app/

# Copy trained model artifacts into container
COPY models /app/models

EXPOSE 8000

# Launch with uvicorn; note main.py is at /app/main.py inside container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
