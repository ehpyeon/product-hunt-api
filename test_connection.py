import requests
import time
import os
from dotenv import load_dotenv

def test_product_hunt_connection():
    """Test basic connectivity to Product Hunt website and API endpoints"""
    print("Testing connection to Product Hunt...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set headers to mimic a browser
    browser_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    endpoints = [
        {"url": "https://www.producthunt.com", "name": "Product Hunt Website"},
        {"url": "https://api.producthunt.com/v2/docs", "name": "API Documentation"},
        {"url": "https://api.producthunt.com/v2/oauth/token", "name": "OAuth Token Endpoint", "method": "OPTIONS"}
    ]
    
    for endpoint in endpoints:
        try:
            method = endpoint.get("method", "GET")
            print(f"\nTesting {endpoint['name']} ({endpoint['url']})...")
            
            if method == "GET":
                response = session.get(endpoint["url"], headers=browser_headers, timeout=10)
            elif method == "OPTIONS":
                response = session.options(endpoint["url"], headers=browser_headers, timeout=10)
            
            print(f"Status code: {response.status_code}")
            print(f"Response size: {len(response.content)} bytes")
            
            # Print headers
            print("Response headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            
            # Check for Cloudflare protection
            if "cf-ray" in response.headers:
                print("\n⚠️ Cloudflare protection detected!")
                print(f"CF-RAY: {response.headers.get('cf-ray')}")
                if response.status_code == 403:
                    print("Cloudflare is blocking the request. This might require browser automation.")
            
            # Wait between requests to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error connecting to {endpoint['name']}: {str(e)}")
    
    print("\n=== Testing OAuth Token Request ===")
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: CLIENT_ID or CLIENT_SECRET not found in .env file")
        return
    
    # Test token request with minimal headers
    try:
        token_url = "https://api.producthunt.com/v2/oauth/token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        
        minimal_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }
        
        print("\nSending token request with minimal headers...")
        response = session.post(token_url, headers=minimal_headers, json=payload, timeout=10)
        
        print(f"Status code: {response.status_code}")
        print("Response headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print("\nResponse body preview:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        
    except Exception as e:
        print(f"Error testing token request: {str(e)}")
    
    print("\nConnection test complete.")

if __name__ == "__main__":
    test_product_hunt_connection()
