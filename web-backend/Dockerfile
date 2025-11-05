# Mausritter API - Docker Image
# Pro deployment na Railway nebo jiný cloud platform

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
# Note: Build context is repo root, so we need to specify web-backend/ path
COPY web-backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from web-backend directory
COPY web-backend/ .

# Copy existing generators from repo root
# (Build context is repo root, so src/ and data/ are directly accessible)
COPY src ./src
COPY data ./data

# Expose port
EXPOSE 8001

# Health check - disabled for Render (they have their own health checks)
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"

# Run FastAPI with uvicorn
# Use $PORT from environment (Render sets this automatically)
# Must use 'python -m uvicorn' because 'uvicorn' is not in shell PATH
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
