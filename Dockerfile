FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY backend/ ./backend/

# Set environment variables
ENV PORT=8080

# Run the application
CMD exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
