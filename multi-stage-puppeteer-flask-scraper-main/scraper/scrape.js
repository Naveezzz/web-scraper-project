const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  const url = process.env.SCRAPE_URL;

  if (!url) {
    console.error("❌ ERROR: SCRAPE_URL environment variable is not set.");
    console.error("Please provide a URL to scrape.");
    process.exit(1);
  }

  console.log("=".repeat(60));
  console.log("🚀 Web Scraper Starting...");
  console.log("=".repeat(60));
  console.log(`🔍 Target URL: ${url}`);
  console.log(`⏰ Started at: ${new Date().toISOString()}`);
  console.log("=".repeat(60));

  try {
    console.log("🌐 Launching headless browser...");
    
    const browser = await puppeteer.launch({
      headless: "new",
      executablePath: "/usr/bin/chromium",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--no-first-run",
        "--no-zygote",
        "--single-process",
        "--disable-extensions"
      ]
    });

    console.log("✅ Browser launched successfully");
    console.log("📄 Opening new page...");

    const page = await browser.newPage();
    
    // Set viewport for consistency
    await page.setViewport({ width: 1280, height: 800 });
    
    console.log(`🔄 Navigating to ${url}...`);
    
    // Navigate to URL with timeout
    await page.goto(url, { 
      waitUntil: "domcontentloaded",
      timeout: 30000
    });

    console.log("✅ Page loaded successfully");
    console.log("📊 Extracting data...");

    // Extract data from page
    const data = await page.evaluate(() => {
      const title = document.title;
      const firstHeading = document.querySelector("h1")
        ? document.querySelector("h1").innerText
        : "No h1 heading found";
      
      // Get meta description if available
      const metaDescription = document.querySelector('meta[name="description"]')
        ? document.querySelector('meta[name="description"]').getAttribute("content")
        : "No meta description found";

      return {
        title: title || "No title found",
        firstHeading,
        metaDescription,
        url: window.location.href,
        scrapedAt: new Date().toISOString()
      };
    });

    console.log("✅ Data extracted successfully");
    console.log("🔒 Closing browser...");
    
    await browser.close();
    
    console.log("✅ Browser closed");
    console.log("💾 Saving data to file...");

    // Ensure output directory exists
    if (!fs.existsSync("/output")) {
      fs.mkdirSync("/output", { recursive: true });
    }

    // Write data to JSON file
    fs.writeFileSync(
      "/output/scraped_data.json",
      JSON.stringify(data, null, 2)
    );

    console.log("=".repeat(60));
    console.log("✅ SUCCESS! Scraping completed");
    console.log("=".repeat(60));
    console.log("📋 Scraped Data:");
    console.log(JSON.stringify(data, null, 2));
    console.log("=".repeat(60));
    console.log(`📁 Data saved to: /output/scraped_data.json`);
    console.log(`⏰ Completed at: ${new Date().toISOString()}`);
    console.log("=".repeat(60));
    
  } catch (error) {
    console.error("=".repeat(60));
    console.error("❌ SCRAPING FAILED");
    console.error("=".repeat(60));
    console.error("Error Type:", error.name);
    console.error("Error Message:", error.message);
    console.error("Stack Trace:", error.stack);
    console.error("=".repeat(60));
    
    // Create error output file
    const errorData = {
      error: true,
      errorType: error.name,
      errorMessage: error.message,
      url: url,
      timestamp: new Date().toISOString()
    };
    
    // Ensure output directory exists
    if (!fs.existsSync("/output")) {
      fs.mkdirSync("/output", { recursive: true });
    }
    
    // Save error information
    fs.writeFileSync(
      "/output/scraped_data.json",
      JSON.stringify(errorData, null, 2)
    );
    
    console.error("💾 Error information saved to /output/scraped_data.json");
    process.exit(1);
  }
})();