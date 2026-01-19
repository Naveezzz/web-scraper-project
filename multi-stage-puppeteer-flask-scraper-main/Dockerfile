# Stage 1: Web Scraping with Node.js and Puppeteer
FROM node:18-slim AS scraper

# Skip Puppeteer's default Chromium download
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install Chromium and required dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    ca-certificates \
    wget \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files and install dependencies
COPY scraper/package.json .
RUN npm install --production

# Copy scraping script
COPY scraper/scrape.js .

# Create output directory
RUN mkdir -p /output

# Define build argument with default value
ARG SCRAPE_URL=https://example.com

# Run the scraping script with the build argument
RUN SCRAPE_URL=${SCRAPE_URL} node scrape.js

# Stage 2: Python Flask Server
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask server file
COPY server/server.py .

# Copy scraped data from first stage
COPY --from=scraper /output/scraped_data.json .

# Expose Flask port
EXPOSE 5000

# Add labels for documentation
LABEL maintainer="your-email@example.com"
LABEL description="Multi-stage Docker build for web scraping with Puppeteer and Flask"
LABEL version="1.0.0"

# Run Flask server
CMD ["python", "server.py"]