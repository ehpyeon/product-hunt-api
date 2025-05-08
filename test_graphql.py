import requests
import json
import os
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

def test_graphql_query():
    """Test a GraphQL query to the Product Hunt API"""
    print("Testing GraphQL query to Product Hunt API...")
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("Error: CLIENT_ID or CLIENT_SECRET not found in .env file")
        return
    
    # Step 1: Get access token
    session = requests.Session()
    
    token_url = "https://api.producthunt.com/v2/oauth/token"
    token_payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    
    token_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    try:
        print("Getting access token...")
        token_response = session.post(token_url, headers=token_headers, json=token_payload)
        
        if token_response.status_code != 200:
            print(f"Failed to get token: {token_response.status_code}")
            print(token_response.text)
            return
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        print(f"Successfully obtained access token: {access_token[:10]}...")
        
        # Step 2: Make GraphQL query
        graphql_url = "https://api.producthunt.com/v2/api/graphql"
        
        # Get date from 7 days ago
        start_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
        
        # GraphQL query
        query = """
        query {
          posts(first: 5, order: VOTES, postedAfter: "2025-05-01T00:00:00Z") {
            edges {
              node {
                name
                tagline
                url
                votesCount
                createdAt
              }
            }
          }
        }
        """
        
        graphql_headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        graphql_payload = {
            "query": query
        }
        
        print("\nSending GraphQL query...")
        print(f"Query: {query}")
        
        # Print the exact request being sent
        print("\nRequest details:")
        print(f"URL: {graphql_url}")
        print(f"Headers: {json.dumps(graphql_headers, indent=2)}")
        print(f"Payload: {json.dumps(graphql_payload, indent=2)}")
        
        graphql_response = session.post(graphql_url, headers=graphql_headers, json=graphql_payload)
        
        print(f"\nResponse status code: {graphql_response.status_code}")
        print("Response headers:")
        for key, value in graphql_response.headers.items():
            print(f"  {key}: {value}")
        
        print("\nResponse body:")
        print(graphql_response.text[:1000] + "..." if len(graphql_response.text) > 1000 else graphql_response.text)
        
        # Try to parse the response as JSON
        try:
            json_response = graphql_response.json()
            print("\nParsed JSON response:")
            print(json.dumps(json_response, indent=2)[:1000] + "..." if len(json.dumps(json_response, indent=2)) > 1000 else json.dumps(json_response, indent=2))
        except json.JSONDecodeError as e:
            print(f"\nFailed to parse response as JSON: {str(e)}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_graphql_query()
