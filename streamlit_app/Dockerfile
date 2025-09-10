# Dockerfile for Streamlit
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY streamlit_app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy all Streamlit app files
COPY streamlit_app /app/streamlit_app

EXPOSE 8501
ENV STREAMLIT_SERVER_HEADLESS=true

# Launch Streamlit
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
