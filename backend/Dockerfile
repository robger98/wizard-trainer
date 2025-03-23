FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
# Since requirements.txt is in the parent directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (we're already in the backend directory)
COPY . ./backend/

# Set environment variables
ENV PORT=8080

# Run the application
CMD exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
