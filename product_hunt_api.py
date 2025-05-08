import requests
import json
import os
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Step 1: Get access token
def get_access_token(client_id, client_secret):
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set minimal headers - this worked in the test script
    minimal_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    url = "https://api.producthunt.com/v2/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    
    try:
        # First, make a GET request to the main site to get cookies
        print("Visiting main site to get cookies...")
        session.get("https://www.producthunt.com")
        
        # Wait a moment to avoid rate limiting
        time.sleep(2)
        
        # Now make the token request with minimal headers
        print("Requesting access token...")
        response = session.post(url, headers=minimal_headers, json=payload)
        
        if response.status_code == 200:
            print("Successfully obtained access token!")
            return response.json().get("access_token")
        else:
            print(f"Error getting token: {response.status_code}")
            print("Response headers:")
            for key, value in response.headers.items():
                print(f"{key}: {value}")
            print("\nResponse body:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print("Response content (if available):")
        if 'response' in locals() and hasattr(response, 'text'):
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        return None

# Step 2: Get products
def get_products(access_token, days_ago=7, limit=10):
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set headers based on what worked in the test script
    graphql_headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Get date from X days ago in UTC
    start_date = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%dT00:00:00Z")
    print(f"Fetching products posted after {start_date}...")
    
    url = "https://api.producthunt.com/v2/api/graphql"
    
    # GraphQL query - using the exact format that worked in the test
    query = f"""
    query {{
      posts(first: {limit}, order: VOTES, postedAfter: "{start_date}") {{
        edges {{
          node {{
            name
            tagline
            url
            votesCount
            createdAt
            description
            thumbnail {{
              url
            }}
          }}
        }}
      }}
    }}
    """
    
    payload = {
        "query": query
    }
    
    try:
        print("Sending GraphQL query...")
        response = session.post(url, headers=graphql_headers, json=payload)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                print(f"Failed to parse response as JSON: {str(e)}")
                print("Response content:")
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                return None
        else:
            print(f"Error fetching products: {response.status_code}")
            print("Response headers:")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")
            print("\nResponse body:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print("Response content (if available):")
        if 'response' in locals() and hasattr(response, 'text'):
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        return None

# Main function
def main():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: CLIENT_ID or CLIENT_SECRET not found in .env file")
        print("Please add your credentials to the .env file")
        return
    
    print(f"Using credentials - Client ID: {client_id[:5]}...")
    print("Getting access token...")
    access_token = get_access_token(client_id, client_secret)
    
    if access_token:
        print("Access token obtained successfully!")
        print("\nFetching recent top products...")
        
        result = get_products(access_token, days_ago=7)
        
        if result and "data" in result and "posts" in result["data"]:
            posts = result["data"]["posts"]["edges"]
            
            print(f"\n{'=' * 50}")
            print(f"TOP PRODUCTS ON PRODUCT HUNT (Last 7 days)")
            print(f"{'=' * 50}")
            
            if not posts:
                print("\nNo products found in the last 7 days. This could be because:")
                print("1. The API might be experiencing issues")
                print("2. Your query parameters might need adjustment")
                print("3. There might be rate limiting in effect")
                print("\nTry modifying the date range or checking the API status.")
            else:
                for i, post in enumerate(posts, 1):
                    node = post["node"]
                    print(f"\n{i}. {node['name']}")
                    print(f"   {node['tagline']}")
                    print(f"   Votes: {node['votesCount']}")
                    print(f"   URL: {node['url']}")
                    print(f"   Created: {node['createdAt']}")
                    if node.get("description"):
                        desc = node['description']
                        if len(desc) > 100:
                            desc = desc[:97] + '...'
                        print(f"   Description: {desc}")
                    if node.get("thumbnail") and node["thumbnail"].get("url"):
                        print(f"   Thumbnail: {node['thumbnail']['url']}")
            
            print(f"\n{'=' * 50}")
            
            # Save raw JSON response for reference
            with open("product_hunt_response.json", "w") as f:
                json.dump(result, f, indent=2)
                print("Raw response saved to product_hunt_response.json")
        else:
            print("No products found or error in response format.")
            print("\nTroubleshooting tips:")
            print("1. Verify your API credentials are correct")
            print("2. Check if your Product Hunt application has the necessary permissions")
            print("3. Try accessing the API through the Product Hunt API Explorer: https://api.producthunt.com/v2/docs")
    else:
        print("Failed to obtain access token. Please check your credentials.")
        print("\nTroubleshooting tips:")
        print("1. Verify your Client ID and Client Secret are correct")
        print("2. Make sure your OAuth application is properly registered")
        print("3. Check if your application has the necessary scopes")
        print("4. Try generating new credentials if the current ones aren't working")
        print("5. The API might be experiencing issues or rate limiting")

# Add a function to test the connection to Product Hunt
def test_connection():
    print("Testing connection to Product Hunt...")
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }
        response = session.get("https://www.producthunt.com", headers=headers)
        print(f"Connection test result: {response.status_code}")
        if response.status_code == 200:
            print("Successfully connected to Product Hunt!")
            return True
        else:
            print("Failed to connect to Product Hunt.")
            return False
    except Exception as e:
        print(f"Connection test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    main()
