# Build stage
FROM python:3.8-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install minimal build dependencies (most packages have pre-built wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
         gcc \
         libffi-dev \
         libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip setuptools==68.0.0 && \
    pip3 install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.8-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
         libjpeg62-turbo \
         libpng16-16 \
         libssl3 && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r sitemanager && useradd -r -g sitemanager sitemanager

WORKDIR /home/website-v3

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY app app 
COPY webapp.py config.py ./ 

ENV FLASK_APP=webapp.py 

RUN chown -R sitemanager:sitemanager ./
USER sitemanager 

EXPOSE 8000 
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "webapp:app", "--workers", "4"]