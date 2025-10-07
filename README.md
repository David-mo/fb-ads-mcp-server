# Facebook Ads MCP Server

A Model Context Protocol (MCP) server that connects AI assistants to Facebook's Ads API. This enables natural language queries to fetch campaign data, insights, and ad performance metrics directly through Claude or other MCP-compatible AI assistants.

## Features

- **Account Management**: List and view details of ad accounts
- **Campaign Tools**: Retrieve campaigns, filter by status, get campaign details
- **Ad Set Tools**: Access ad sets within campaigns with targeting information
- **Ad Tools**: View individual ads and their creative details
- **Insights & Analytics**: Get performance metrics (impressions, clicks, spend, CTR, etc.)
- **Pagination Support**: Handle large datasets with pagination helpers
- **Error Handling**: Comprehensive error messages and rate limit handling

## Prerequisites

- Python 3.10 or higher
- Facebook Developer account with Ads API access
- Facebook Access Token with `ads_read` permission

## Installation

### 1. Clone or Download

```bash
cd fb-ads-mcp-server
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Getting Your Facebook Access Token

### Option 1: Graph API Explorer (Quick Testing)

1. Go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app or create a new one
3. Click "Generate Access Token"
4. Add the `ads_read` permission
5. Copy the generated token

**Note**: Tokens from Graph API Explorer expire in 1-2 hours. For production use, implement a proper OAuth flow.

### Option 2: Meta Developer Portal (Long-lived Tokens)

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create or select an app
3. Navigate to **Tools** → **Access Token Tool**
4. Generate a User Access Token with `ads_read` permission
5. Optionally exchange for a long-lived token (60 days)

### Required Permissions

- `ads_read` - Read access to ad accounts, campaigns, and insights

## Running the Server

### Local Testing

```bash
python server.py --fb-token YOUR_FACEBOOK_ACCESS_TOKEN
```

The server will start and listen for MCP protocol requests.

## Claude Desktop Configuration

To use this MCP server with Claude Desktop, add the following to your Claude configuration file:

### macOS/Linux

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/fb-ads-mcp-server/server.py",
        "--fb-token",
        "YOUR_FACEBOOK_ACCESS_TOKEN"
      ]
    }
  }
}
```

### Windows

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "command": "python",
      "args": [
        "C:\\absolute\\path\\to\\fb-ads-mcp-server\\server.py",
        "--fb-token",
        "YOUR_FACEBOOK_ACCESS_TOKEN"
      ]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/fb-ads-mcp-server/server.py` with the actual absolute path to your `server.py` file.

### Using Virtual Environment with Claude Desktop

If you want to use the virtual environment with Claude Desktop:

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "command": "/absolute/path/to/fb-ads-mcp-server/venv/bin/python",
      "args": [
        "/absolute/path/to/fb-ads-mcp-server/server.py",
        "--fb-token",
        "YOUR_FACEBOOK_ACCESS_TOKEN"
      ]
    }
  }
}
```

## Available Tools

### Account Management

- **list_ad_accounts()** - Lists all ad accounts linked to your access token
- **get_details_of_ad_account(act_id, fields)** - Get detailed information about a specific ad account

### Campaign Management

- **get_campaigns_by_adaccount(act_id, fields, limit, filtering)** - Retrieve all campaigns for an ad account
- **get_campaign_by_id(campaign_id, fields)** - Get details for a specific campaign

### Ad Set Management

- **get_adsets_by_campaign(campaign_id, fields, limit)** - Retrieve all ad sets within a campaign
- **get_adset_by_id(adset_id, fields)** - Get details for a specific ad set

### Ad Management

- **get_ads_by_adset(adset_id, fields, limit)** - Retrieve all ads within an ad set
- **get_ad_by_id(ad_id, fields)** - Get details for a specific ad

### Insights & Analytics

- **get_campaign_insights(campaign_id, fields, date_preset, time_range)** - Get performance metrics for a campaign
- **get_adset_insights(adset_id, fields, date_preset)** - Get performance metrics for an ad set
- **get_ad_insights(ad_id, fields, date_preset)** - Get performance metrics for a specific ad
- **get_summary_report(act_id, date_preset, time_range, limit)** - Get lightweight summary with only key metrics (optimized to avoid context limits)

### Pagination

- **fetch_pagination_url(url)** - Fetch next/previous page of results

## Usage Examples

Once configured with Claude Desktop, you can ask natural language questions:

### Basic Queries

```
"List my Facebook ad accounts"
"Show me all campaigns for account act_123456789"
"Get the active campaigns for my ad account"
```

### Filtering & Details

```
"Show me only active campaigns for account act_123456789"
"Get details for campaign 120210000000001"
"What ad sets are in campaign 120210000000001?"
```

### Insights & Analytics

```
"Show me insights for campaign 120210000000001 for the last 7 days"
"Get performance metrics for ad set 120210000000002"
"What's the CTR and spend for ad 120210000000003?"
```

### Custom Fields

```
"Get campaigns with fields: name, status, budget_remaining, created_time"
"Show ad account details with fields: name, currency, timezone_name"
```

### Date Ranges

```
"Get campaign insights for last_30d"
"Show me lifetime performance for this ad set"
"Get insights from 2024-01-01 to 2024-01-31"
```

## Common Field Names

### Campaign Fields
- `name`, `objective`, `status`, `effective_status`
- `daily_budget`, `lifetime_budget`, `budget_remaining`
- `created_time`, `updated_time`, `start_time`, `stop_time`

### Ad Set Fields
- `name`, `effective_status`, `optimization_goal`
- `daily_budget`, `lifetime_budget`
- `targeting`, `bid_amount`, `billing_event`

### Ad Fields
- `name`, `effective_status`, `creative`
- `tracking_specs`, `conversion_specs`

### Insight Metrics
- `impressions`, `clicks`, `spend`, `reach`, `frequency`
- `cpc` (Cost Per Click), `cpm` (Cost Per 1000 Impressions)
- `ctr` (Click-Through Rate), `conversions`, `cost_per_conversion`

### Date Presets
- `today`, `yesterday`
- `last_7d`, `last_14d`, `last_30d`, `last_90d`
- `this_month`, `last_month`
- `this_quarter`, `last_quarter`
- `this_year`, `last_year`
- `lifetime`

## Error Handling

The server includes comprehensive error handling for:

- **Missing Token**: Clear error message if `--fb-token` is not provided
- **Invalid Token**: Facebook API errors are caught and formatted clearly
- **Rate Limits**: HTTP 429 errors are properly handled
- **Network Errors**: Timeout and connection errors include helpful messages
- **Invalid Parameters**: Type validation and required field checking

## Security Best Practices

1. **Never Commit Tokens**: The `.gitignore` file excludes `.env` files and logs
2. **Minimum Permissions**: Use tokens with only `ads_read` permission for read-only access
3. **Token Rotation**: Regularly rotate your access tokens
4. **Secure Storage**: Store tokens securely; avoid hardcoding in configuration files
5. **Monitor Usage**: Check your Meta Developer dashboard for unusual API activity

## Troubleshooting

### "Facebook access token not provided"

Make sure you're running the server with the `--fb-token` argument:
```bash
python server.py --fb-token YOUR_TOKEN
```

### "Invalid OAuth access token"

Your token may have expired. Generate a new token from the Graph API Explorer or Meta Developer Portal.

### "Unsupported get request"

Check that your account IDs are in the correct format (e.g., `act_123456789`).

### Rate Limit Errors

Facebook has rate limits on API calls. If you hit limits, wait a few minutes before retrying. Consider implementing caching for frequently accessed data.

## API Version

This server uses **Facebook Graph API v22.0**. Check [Facebook's API Changelog](https://developers.facebook.com/docs/graph-api/changelog) for version updates.

## Limitations

- **Read-Only**: This server only supports read operations. Write operations (creating/updating campaigns) require additional permissions and implementation.
- **Token Expiration**: Short-lived tokens expire in 1-2 hours. Implement token refresh logic for production use.
- **Rate Limits**: Subject to Facebook's API rate limits based on your app tier.

## Future Enhancements

- Token refresh automation
- Write operations (create/update campaigns, ad sets, ads)
- Webhook support for real-time updates
- Response caching layer
- Bulk operations for efficiency
- Custom audience management
- Ad creative operations
- Activity/change history tracking

## Contributing

Contributions are welcome! Areas for improvement:

- Enhanced error messages and retry logic
- Additional API endpoints (custom audiences, pixels, etc.)
- Performance optimizations and caching
- Write operation support
- Automated testing suite

## License

This project is provided as-is for educational and development purposes.

## Resources

- [Facebook Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## Support

For issues related to:
- **This MCP Server**: Open an issue in this repository
- **Facebook API**: Check [Facebook Developer Community](https://developers.facebook.com/community/)
- **MCP Protocol**: Visit [MCP Documentation](https://modelcontextprotocol.io/)

---

**Happy advertising! 🚀**

