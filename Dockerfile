# Multi-stage build for faster deployment
FROM python:3.11-slim as base

# Install system dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Install Python dependencies (cache this layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base as production

# Copy application code (changes frequently)
COPY backend/app ./app
COPY backend/templates ./templates

# Create directories
RUN mkdir -p /tmp/uploads /tmp/output

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app /tmp
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
