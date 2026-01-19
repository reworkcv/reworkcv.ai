# Resume Tailor Backend Dockerfile - Cloud Run Optimized
FROM python:3.11-slim

# Install system dependencies including pdflatex for PDF generation
RUN apt-get update && apt-get install -y \
    libmagic1 \
    file \
    curl \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy requirements first (for better caching)
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/app ./app
COPY backend/templates ./templates

# Create directories for uploads and output (use /tmp for Cloud Run)
RUN mkdir -p /tmp/uploads /tmp/output

# Create non-root user for Cloud Run security
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app /tmp/uploads /tmp/output
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Start FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
