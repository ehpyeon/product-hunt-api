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

## Troubleshooting

If you encounter issues with the API:

1. Run the test scripts to diagnose connection issues:
   ```
   python3 test_connection.py
   python3 test_graphql.py
   ```

2. Check that your API credentials are correct in the `.env` file

3. The API might be rate-limited or have Cloudflare protection - the script includes measures to handle this
