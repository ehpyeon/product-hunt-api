# Product Hunt API Client

This script fetches top products from Product Hunt using their GraphQL API. It demonstrates how to authenticate with the Product Hunt API and make GraphQL queries to retrieve product data.

## Setup

1. Activate the virtual environment:
   ```
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   .\venv\Scripts\activate
   ```

2. Register an OAuth application on Product Hunt:
   - Go to https://www.producthunt.com/v2/oauth/applications
   - Create a new application
   - Get your Client ID and Client Secret

3. Update the .env file with your credentials:
   - Open `.env`
   - Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with your actual credentials

## Usage

Run the script:
```
python3 product_hunt_api.py
```

The script will:
1. Obtain an access token using your credentials
2. Fetch recent top products from Product Hunt (last 7 days)
3. Display the results in a formatted list
4. Save the raw JSON response to `product_hunt_response.json`

## Customization

You can modify the script to change:
- The number of products to fetch (change the `limit` parameter in `get_products()`)
- The date range (modify the `days_ago` parameter in `get_products()`)
- The sort order (modify the `order` parameter in the GraphQL query)
- The data fields you want to retrieve (add or remove fields in the GraphQL query)

## API Request and Response Format

### Authentication Request

```json
// POST https://api.producthunt.com/v2/oauth/token
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "grant_type": "client_credentials"
}
```

### Authentication Response

```json
{
  "access_token": "IiU1rMMq6qu66vE9wlZJQ5abI6PEpL4k0kHY6zJLtGo",
  "token_type": "Bearer",
  "scope": "public",
  "created_at": 1746665909
}
```

### GraphQL Request

```json
// POST https://api.producthunt.com/v2/api/graphql
// Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
{
  "query": "query { posts(first: 10, order: VOTES, postedAfter: \"2025-05-01T00:00:00Z\") { edges { node { name tagline url votesCount createdAt description thumbnail { url } } } } }"
}
```

### GraphQL Response Structure

```json
{
  "data": {
    "posts": {
      "edges": [
        {
          "node": {
            "name": "Product Name",
            "tagline": "Product Tagline",
            "url": "Product URL",
            "votesCount": 123,
            "createdAt": "2025-05-01T07:01:00Z",
            "description": "Product Description",
            "thumbnail": {
              "url": "Thumbnail URL"
            }
          }
        },
        // More products...
      ]
    }
  }
}
```

### Real Response Example

```json
{
  "data": {
    "posts": {
      "edges": [
        {
          "node": {
            "name": "Raycast for iOS",
            "tagline": "Powerful productivity on the go",
            "url": "https://www.producthunt.com/posts/raycast-for-ios?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+AI+Feed+%28ID%3A+187654%29",
            "votesCount": 801,
            "createdAt": "2025-05-01T07:01:00Z",
            "description": "Introducing Raycast for iOS: Your all-in-one productivity toolkit with AI, Notes, and more – now on mobile as the perfect companion to the macOS app.",
            "thumbnail": {
              "url": "https://ph-files.imgix.net/14515c52-8217-4e1e-813e-77a18abc6e82.png?auto=format"
            }
          }
        },
        {
          "node": {
            "name": "Postiz v2",
            "tagline": "Social Media Scheduling with MCP support",
            "url": "https://www.producthunt.com/posts/postiz-v2?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+AI+Feed+%28ID%3A+187654%29",
            "votesCount": 762,
            "createdAt": "2025-05-01T07:01:00Z",
            "description": "Your ultimate AI social media scheduling tool, 20+ available socials! Plus: MCPs, auto-reposts, repeated posts, AI agents, quick image generation, and auto short-linking.",
            "thumbnail": {
              "url": "https://ph-files.imgix.net/af39c728-20de-40d5-8540-1c4d862fc99d.png?auto=format"
            }
          }
        }
        // More products...
      ]
    }
  }
}
```

## Troubleshooting

If you encounter issues with the API:

1. Run the test scripts to diagnose connection issues:
   ```
   python3 test_connection.py
   python3 test_graphql.py
   ```

2. Check that your API credentials are correct in the `.env` file

3. The API might be rate-limited or have Cloudflare protection - the script includes measures to handle this
