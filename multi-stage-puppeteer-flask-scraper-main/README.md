# Multi-Stage Web Scraper API

This project is a Dockerized web scraper that demonstrates the power of a multi-stage build using Node.js (Puppeteer) for scraping and Python (Flask) for serving content.

---

## Technologies Used

- Node.js + Puppeteer for headless web scraping
- Python + Flask for serving scraped data
- Multi-stage Docker build to keep final image lean
- Chromium installed via `apt` for Puppeteer

---

## How It Works

1. Accepts a `SCRAPE_URL` as a build argument
2. Uses Puppeteer to scrape the title and first `<h1>` of the target page
3. Outputs a `scraped_data.json` file
4. Flask reads the JSON and serves it via a REST API

---

## Project Structure
.
├── Dockerfile
├── README.md
├── scraper
│   ├── package.json
│   └── scrape.js
└── server
    ├── requirements.txt
    └── server.py

3 directories, 6 files

## Build Docker Image

```bash
docker build --build-arg SCRAPE_URL="https://example.com" -t scraper-api .

##  Run the Container

```bash
docker run -p 5000:5000 scraper-api:latest

##  Example Output

{
  "title": "Hacker News",
  "firstHeading": "Hacker News"
}
