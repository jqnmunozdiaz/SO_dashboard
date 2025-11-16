# Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# No system build tools needed (keeps image small and speeds build)

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Speed up installs and prefer wheels when available
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 dashuser && chown -R dashuser:dashuser /app
USER dashuser

# Expose app port (Cloud Run sets PORT env var)
EXPOSE 8080

# Set environment variables
ENV ENVIRONMENT=production
ENV PORT=8080

# Run the application
CMD ["python", "app.py"]
