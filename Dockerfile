# Use Python 3.11 for better performance and security updates
FROM python:3.11-slim

# Set environment variables for Python optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy and install requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .streamlit directory and config for optimal Cloud Run performance
RUN mkdir -p /home/appuser/.streamlit && \
    echo '[server]\n\
port = 8080\n\
address = "0.0.0.0"\n\
headless = true\n\
fileWatcherType = "none"\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
base = "light"\n' > /home/appuser/.streamlit/config.toml

# Change ownership to non-root user
RUN chown -R appuser:appuser /app /home/appuser

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "Home.py"]