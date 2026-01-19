from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

SCRAPED_FILE = "scraped_data.json"

def load_scraped_data():
    """Load scraped data from JSON file"""
    try:
        if not os.path.exists(SCRAPED_FILE):
            return None, "File not found"
        
        with open(SCRAPED_FILE, "r") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

@app.route("/")
def home():
    """Main endpoint - serve scraped data with metadata"""
    data, error = load_scraped_data()
    
    if error:
        return jsonify({
            "status": "error",
            "error": error,
            "message": "Failed to load scraped data",
            "timestamp": datetime.utcnow().isoformat()
        }), 500
    
    # Check if scraping failed
    if data.get("error"):
        return jsonify({
            "status": "scraping_failed",
            "error": data.get("errorMessage", "Unknown error"),
            "details": data,
            "timestamp": datetime.utcnow().isoformat()
        }), 500
    
    # Return successful data
    response = {
        "status": "success",
        "message": "Data retrieved successfully",
        "data": data,
        "server_info": {
            "server_time": datetime.utcnow().isoformat(),
            "data_source": SCRAPED_FILE
        }
    }
    
    return jsonify(response), 200

@app.route("/raw")
def raw():
    """Raw endpoint - serve scraped data without wrapper"""
    data, error = load_scraped_data()
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify(data), 200

@app.route("/health")
def health():
    """Health check endpoint"""
    data, error = load_scraped_data()
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "data_file_exists": os.path.exists(SCRAPED_FILE),
        "data_loadable": error is None
    }
    
    if error:
        health_status["status"] = "degraded"
        health_status["warning"] = error
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200

@app.route("/info")
def info():
    """Information endpoint about the API"""
    return jsonify({
        "api_name": "Web Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "/": "Get scraped data with metadata",
            "/raw": "Get raw scraped data",
            "/health": "Health check endpoint",
            "/info": "API information"
        },
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": ["/", "/raw", "/health", "/info"],
        "timestamp": datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(e),
        "timestamp": datetime.utcnow().isoformat()
    }), 500

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Flask Server Starting...")
    print("=" * 60)
    print(f"📁 Scraped data file: {os.path.abspath(SCRAPED_FILE)}")
    print(f"📂 Current directory: {os.getcwd()}")
    print(f"📋 Files in directory: {', '.join(os.listdir('.'))}")
    print(f"✅ File exists: {os.path.exists(SCRAPED_FILE)}")
    
    if os.path.exists(SCRAPED_FILE):
        file_size = os.path.getsize(SCRAPED_FILE)
        print(f"📊 File size: {file_size} bytes")
    
    print("=" * 60)
    print("📡 API Endpoints Available:")
    print("   GET /        - Scraped data with metadata")
    print("   GET /raw     - Raw scraped data")
    print("   GET /health  - Health check")
    print("   GET /info    - API information")
    print("=" * 60)
    print("🌐 Server will be accessible at: http://0.0.0.0:5000")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5000, debug=False)