"""
Facebook Ads MCP Server

A Model Context Protocol server that connects AI assistants to Facebook's Ads API.
Enables natural language queries to fetch campaign data, insights, and ad performance metrics.

Supports both local (stdio) and remote (SSE) deployment.
"""

from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, List, Optional, Any
import sys
import json
import os

# Constants
FB_API_VERSION = "v22.0"
FB_GRAPH_URL = f"https://graph.facebook.com/{FB_API_VERSION}"

# Initialize MCP server
mcp = FastMCP("fb-ads-mcp-server")

# Global token storage
FB_ACCESS_TOKEN = None


def _get_fb_access_token() -> str:
    """
    Get Facebook access token from environment variable or command line arguments.
    Cache in memory after first read.
    
    Priority:
    1. Environment variable FB_ACCESS_TOKEN (for Railway/cloud deployment)
    2. Command line argument --fb-token (for local use)
    
    Expects: python server.py --fb-token YOUR_TOKEN
    
    Returns:
        str: Facebook access token
        
    Raises:
        ValueError: If token is not provided
    """
    global FB_ACCESS_TOKEN
    
    if FB_ACCESS_TOKEN is None:
        # Priority 1: Check environment variable (for cloud deployment)
        FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
        
        # Priority 2: Parse --fb-token from sys.argv (for local use)
        if not FB_ACCESS_TOKEN:
            try:
                token_index = sys.argv.index('--fb-token')
                if token_index + 1 < len(sys.argv):
                    FB_ACCESS_TOKEN = sys.argv[token_index + 1]
                else:
                    raise ValueError("--fb-token flag provided but no token value found")
            except ValueError as e:
                if "--fb-token" in str(e):
                    raise e
                raise ValueError(
                    "Facebook access token not provided. "
                    "Set FB_ACCESS_TOKEN environment variable or run with: python server.py --fb-token YOUR_TOKEN"
                )
        
        # Validate token is not empty
        if not FB_ACCESS_TOKEN or FB_ACCESS_TOKEN.strip() == '':
            raise ValueError("Facebook access token cannot be empty")
    
    return FB_ACCESS_TOKEN


def _make_graph_api_call(url: str, params: Dict) -> Dict:
    """
    Centralized Facebook Graph API caller.
    Handles errors and returns JSON.
    
    Args:
        url: The Graph API endpoint URL
        params: Query parameters including access token
        
    Returns:
        Dict: JSON response from the API
        
    Raises:
        requests.HTTPError: If the API returns an error status code
        requests.RequestException: For network-related errors
    """
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Try to extract Facebook-specific error message
        try:
            error_data = e.response.json()
            if 'error' in error_data:
                error_msg = error_data['error'].get('message', str(e))
                error_code = error_data['error'].get('code', 'unknown')
                raise requests.HTTPError(
                    f"Facebook API Error (Code {error_code}): {error_msg}",
                    response=e.response
                )
        except (ValueError, KeyError):
            pass
        raise
    except requests.exceptions.Timeout:
        raise requests.RequestException("Request to Facebook API timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"Network error calling Facebook API: {str(e)}")


# =============================================================================
# ACCOUNT MANAGEMENT TOOLS
# =============================================================================

@mcp.tool()
def list_ad_accounts() -> Dict:
    """
    Lists all ad accounts linked to the access token.
    
    Returns:
        Dict: JSON response containing ad accounts with name, account_id, 
              account_status, and currency fields
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/me/adaccounts"
    params = {
        'access_token': access_token,
        'fields': 'name,account_id,account_status,currency'
    }
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_details_of_ad_account(act_id: str, fields: Optional[List[str]] = None) -> Dict:
    """
    Get detailed information about a specific ad account.
    
    Args:
        act_id: Account ID (format: act_1234567890)
        fields: Optional list of fields to retrieve. If not provided, 
                defaults to: name, account_status, amount_spent, balance, currency
    
    Returns:
        Dict: JSON response with requested ad account details
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}"
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'name,account_status,amount_spent,balance,currency'
    
    return _make_graph_api_call(url, params)


# =============================================================================
# CAMPAIGN TOOLS
# =============================================================================

@mcp.tool()
def get_campaigns_by_adaccount(
    act_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25,
    filtering: Optional[List[dict]] = None
) -> Dict:
    """
    Retrieve all campaigns for an ad account.
    
    Args:
        act_id: Account ID (format: act_1234567890)
        fields: Optional list of fields to retrieve
        limit: Max results per page (default: 25)
        filtering: Optional filters. Example:
                  [{"field":"effective_status","operator":"IN","value":["ACTIVE"]}]
    
    Returns:
        Dict: JSON response containing campaigns data with pagination info
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{act_id}/campaigns"
    
    params = {
        'access_token': access_token,
        'limit': limit
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'name,objective,status,effective_status,daily_budget,lifetime_budget'
    
    if filtering:
        params['filtering'] = json.dumps(filtering)
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_campaign_by_id(campaign_id: str, fields: Optional[List[str]] = None) -> Dict:
    """
    Get details for a specific campaign.
    
    Args:
        campaign_id: Campaign ID
        fields: Optional list of fields to retrieve
    
    Returns:
        Dict: JSON response with campaign details
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}"
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    
    return _make_graph_api_call(url, params)


# =============================================================================
# AD SET TOOLS
# =============================================================================

@mcp.tool()
def get_adsets_by_campaign(
    campaign_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25
) -> Dict:
    """
    Retrieve all ad sets within a campaign.
    
    Args:
        campaign_id: Campaign ID
        fields: Optional list of fields to retrieve
        limit: Max results per page (default: 25)
    
    Returns:
        Dict: JSON response containing ad sets data
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/adsets"
    
    params = {
        'access_token': access_token,
        'limit': limit
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'name,effective_status,daily_budget,lifetime_budget,targeting'
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_adset_by_id(adset_id: str, fields: Optional[List[str]] = None) -> Dict:
    """
    Get details for a specific ad set.
    
    Args:
        adset_id: Ad Set ID
        fields: Optional list of fields to retrieve
    
    Returns:
        Dict: JSON response with ad set details
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}"
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    
    return _make_graph_api_call(url, params)


# =============================================================================
# AD TOOLS
# =============================================================================

@mcp.tool()
def get_ads_by_adset(
    adset_id: str,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = 25
) -> Dict:
    """
    Retrieve all ads within an ad set.
    
    Args:
        adset_id: Ad Set ID
        fields: Optional list of fields to retrieve
        limit: Max results per page (default: 25)
    
    Returns:
        Dict: JSON response containing ads data
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/ads"
    
    params = {
        'access_token': access_token,
        'limit': limit
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'name,effective_status,creative'
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ad_by_id(ad_id: str, fields: Optional[List[str]] = None) -> Dict:
    """
    Get details for a specific ad.
    
    Args:
        ad_id: Ad ID
        fields: Optional list of fields to retrieve
    
    Returns:
        Dict: JSON response with ad details
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}"
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    
    return _make_graph_api_call(url, params)


# =============================================================================
# INSIGHTS TOOLS
# =============================================================================

@mcp.tool()
def get_campaign_insights(
    campaign_id: str,
    fields: Optional[List[str]] = None,
    date_preset: Optional[str] = "last_30d",
    time_range: Optional[Dict[str, str]] = None
) -> Dict:
    """
    Get performance insights for a campaign.
    
    Args:
        campaign_id: Campaign ID
        fields: Metrics to retrieve (e.g., ['impressions', 'clicks', 'spend'])
                Default: impressions, clicks, spend, cpc, cpm, ctr, reach
        date_preset: Date range preset (e.g., 'last_7d', 'last_30d', 'lifetime')
        time_range: Custom date range (e.g., {"since":"2024-01-01","until":"2024-01-31"})
                   If provided, overrides date_preset
    
    Returns:
        Dict: JSON response with campaign insights data
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{campaign_id}/insights"
    
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'impressions,clicks,spend,cpc,cpm,ctr,reach'
    
    if time_range:
        params['time_range'] = json.dumps(time_range)
    elif date_preset:
        params['date_preset'] = date_preset
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_adset_insights(
    adset_id: str,
    fields: Optional[List[str]] = None,
    date_preset: Optional[str] = "last_30d"
) -> Dict:
    """
    Get performance insights for an ad set.
    
    Args:
        adset_id: Ad Set ID
        fields: Metrics to retrieve (e.g., ['impressions', 'clicks', 'spend'])
        date_preset: Date range preset (e.g., 'last_7d', 'last_30d', 'lifetime')
    
    Returns:
        Dict: JSON response with ad set insights data
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{adset_id}/insights"
    
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'impressions,clicks,spend,cpc,ctr'
    
    if date_preset:
        params['date_preset'] = date_preset
    
    return _make_graph_api_call(url, params)


@mcp.tool()
def get_ad_insights(
    ad_id: str,
    fields: Optional[List[str]] = None,
    date_preset: Optional[str] = "last_30d"
) -> Dict:
    """
    Get performance insights for a specific ad.
    
    Args:
        ad_id: Ad ID
        fields: Metrics to retrieve (e.g., ['impressions', 'clicks', 'spend'])
        date_preset: Date range preset (e.g., 'last_7d', 'last_30d', 'lifetime')
    
    Returns:
        Dict: JSON response with ad insights data
    """
    access_token = _get_fb_access_token()
    url = f"{FB_GRAPH_URL}/{ad_id}/insights"
    
    params = {'access_token': access_token}
    
    if fields:
        params['fields'] = ','.join(fields)
    else:
        params['fields'] = 'impressions,clicks,spend,cpc,ctr'
    
    if date_preset:
        params['date_preset'] = date_preset
    
    return _make_graph_api_call(url, params)


# =============================================================================
# COMPREHENSIVE AD REPORT
# =============================================================================

@mcp.tool()
def get_comprehensive_ad_report(
    act_id: str,
    date_preset: Optional[str] = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    campaign_id: Optional[str] = None,
    limit: Optional[int] = 100,
    min_spend: Optional[float] = 0
) -> Dict:
    """
    Get comprehensive ad performance report with all metrics and details.
    
    Returns detailed data for all ads including:
    - Ad Creative ID, Ad ID, Ad Name
    - Campaign ID, Campaign Name
    - Ad Set ID, Ad Set Name
    - Ad Status, Delivery
    - Asset URL (image/video)
    - Reach, Impressions, Frequency
    - Purchases, Cost Per Purchase (flexible based on conversion events)
    - Clicks (All), Unique Clicks, CTR, Unique CTR, CPC, CPM
    - Video metrics (3s plays, 25%/50%/75%/100% completion, ThruPlays)
    - Conversions (Add to Cart, Content Views, Checkouts Initiated)
    - Landing Page Views, Link Clicks, Outbound Clicks
    - Engagement (Post Reactions, Comments, Saves, Shares, Post Engagement, Page Likes)
    - Amount Spent
    
    Args:
        act_id: Account ID (format: act_1234567890)
        date_preset: Date range preset (default: 'last_30d'). Options: 'today', 'yesterday', 
                     'last_7d', 'last_14d', 'last_30d', 'last_90d', 'lifetime', etc.
        time_range: Custom date range (e.g., {"since":"2024-01-01","until":"2024-01-31"})
        campaign_id: Optional campaign ID to filter by specific campaign
        limit: Max number of ads to retrieve (default: 100)
        min_spend: Minimum spend threshold (default: 0, only returns ads with spend > this value)
    
    Returns:
        Dict: Comprehensive ad report with all requested fields
        
    Example:
        To get all ads with spend from an account for the last 30 days:
        get_comprehensive_ad_report("act_123456789")
        
        To get ads with at least $100 spend in last 7 days:
        get_comprehensive_ad_report("act_123456789", date_preset="last_7d", min_spend=100)
    """
    access_token = _get_fb_access_token()
    
    # Define all the fields we want from the ad object itself
    ad_fields = [
        'id',
        'name',
        'status',
        'effective_status',
        'campaign_id',
        'campaign{id,name}',
        'adset_id',
        'adset{id,name}',
        'creative{id,asset_feed_spec,image_url,video_id,thumbnail_url,object_story_spec}'
    ]
    
    # Define all insight metrics
    insight_fields = [
        'reach', 'impressions', 'frequency', 'spend',
        'clicks', 'unique_clicks', 'ctr', 'unique_ctr', 'cpc', 'cpm',
        'video_play_actions', 'video_thruplay_watched_actions',
        'video_p25_watched_actions', 'video_p50_watched_actions',
        'video_p75_watched_actions', 'video_p100_watched_actions',
        'video_continuous_2_sec_watched_actions',
        'actions', 'action_values', 'cost_per_action_type'
    ]
    
    # First, get all ads (or ads within a specific campaign)
    ads_url = f"{FB_GRAPH_URL}/{campaign_id}/ads" if campaign_id else f"{FB_GRAPH_URL}/{act_id}/ads"
    ads_params = {
        'access_token': access_token,
        'fields': ','.join(ad_fields),
        'limit': limit
    }
    ads_response = _make_graph_api_call(ads_url, ads_params)
    all_ads = {ad['id']: ad for ad in ads_response.get('data', [])}
    
    # Now fetch insights for all relevant ads in one call with breakdown by ad
    insights_url = f"{FB_GRAPH_URL}/{act_id}/insights"
    insights_params = {
        'access_token': access_token,
        'level': 'ad',
        'fields': ','.join(insight_fields),
        'limit': limit,
        'filtering': json.dumps([{
            'field': 'spend',
            'operator': 'GREATER_THAN',
            'value': min_spend
        }])
    }
    
    if time_range:
        insights_params['time_range'] = json.dumps(time_range)
    elif date_preset:
        insights_params['date_preset'] = date_preset
    
    all_insights_response = _make_graph_api_call(insights_url, insights_params)
    insights_by_ad_id = {
        insight['ad_id']: insight
        for insight in all_insights_response.get('data', [])
    }
    
    results = []
    for ad_id, ad in all_ads.items():
        insights_data = insights_by_ad_id.get(ad_id, {})
        
        # Skip ads that didn't have spend (due to filtering in insights call)
        if not insights_data:
            continue
        
        # Extract asset URL from creative
        asset_url = None
        creative = ad.get('creative', {})
        if creative:
            asset_url = creative.get('thumbnail_url') or creative.get('image_url')
            if not asset_url and creative.get('object_story_spec'):
                video_data = creative.get('object_story_spec', {}).get('video_data', {})
                if video_data:
                    asset_url = f"Video ID: {video_data.get('video_id', 'N/A')}"
        
        def get_action_value(actions_list, action_type):
            if not actions_list:
                return None
            for action in actions_list:
                if action_type in action.get('action_type', ''):
                    return action.get('value')
            return None
        
        def get_cost_per_action(cost_per_actions, action_type):
            if not cost_per_actions:
                return None
            for action in cost_per_actions:
                if action_type in action.get('action_type', ''):
                    return action.get('value')
            return None
        
        actions = insights_data.get('actions', [])
        video_actions = insights_data.get('video_play_actions', [])
        cost_per_actions = insights_data.get('cost_per_action_type', [])
        
        # Try to get primary conversion (purchase first, then other conversion events)
        purchases = (get_action_value(actions, 'purchase') or 
                    get_action_value(actions, 'offsite_conversion.fb_pixel_purchase') or
                    get_action_value(actions, 'offsite_conversion') or
                    get_action_value(actions, 'onsite_conversion'))
        
        cost_per_purchase = (get_cost_per_action(cost_per_actions, 'purchase') or
                            get_cost_per_action(cost_per_actions, 'offsite_conversion.fb_pixel_purchase') or
                            get_cost_per_action(cost_per_actions, 'offsite_conversion') or
                            get_cost_per_action(cost_per_actions, 'onsite_conversion'))
        
        result = {
            'ad_creative_id': creative.get('id') if creative else None,
            'ad_id': ad_id,
            'ad_name': ad.get('name'),
            'campaign_id': ad.get('campaign', {}).get('id') if ad.get('campaign') else ad.get('campaign_id'),
            'campaign_name': ad.get('campaign', {}).get('name') if ad.get('campaign') else None,
            'ad_set_id': ad.get('adset', {}).get('id') if ad.get('adset') else ad.get('adset_id'),
            'ad_set_name': ad.get('adset', {}).get('name') if ad.get('adset') else None,
            'ad_status': ad.get('status'),
            'delivery': ad.get('effective_status'),
            'asset_url': asset_url,
            
            'reach': insights_data.get('reach'),
            'impressions': insights_data.get('impressions'),
            'frequency': insights_data.get('frequency'),
            'purchases': purchases,
            'cost_per_purchase': cost_per_purchase,
            'clicks_all': insights_data.get('clicks'),
            'unique_clicks_all': insights_data.get('unique_clicks'),
            'ctr_all': insights_data.get('ctr'),
            'unique_ctr_all': insights_data.get('unique_ctr'),
            'cpc_all': insights_data.get('cpc'),
            'cpm': insights_data.get('cpm'),
            
            'video_3_sec_plays': get_action_value(insights_data.get('video_continuous_2_sec_watched_actions', []), 'video_view'),
            'video_plays_25_percent': get_action_value(insights_data.get('video_p25_watched_actions', []), 'video_view'),
            'video_plays_50_percent': get_action_value(insights_data.get('video_p50_watched_actions', []), 'video_view'),
            'video_plays_75_percent': get_action_value(insights_data.get('video_p75_watched_actions', []), 'video_view'),
            'video_plays_100_percent': get_action_value(insights_data.get('video_p100_watched_actions', []), 'video_view'),
            'video_plays': get_action_value(video_actions, 'video_view'),
            'thru_plays': get_action_value(insights_data.get('video_thruplay_watched_actions', []), 'video_view'),
            
            'adds_to_cart': get_action_value(actions, 'add_to_cart') or get_action_value(actions, 'offsite_conversion.fb_pixel_add_to_cart'),
            'content_views': get_action_value(actions, 'view_content') or get_action_value(actions, 'offsite_conversion.fb_pixel_view_content'),
            'checkouts_initiated': get_action_value(actions, 'initiate_checkout') or get_action_value(actions, 'offsite_conversion.fb_pixel_initiate_checkout'),
            'landing_page_views': get_action_value(actions, 'landing_page_view'),
            'link_clicks': get_action_value(actions, 'link_click'),
            'outbound_clicks': get_action_value(actions, 'outbound_click'),
            
            'post_reactions': get_action_value(actions, 'post_reaction'),
            'post_comments': get_action_value(actions, 'comment'),
            'post_saves': get_action_value(actions, 'post_save'),
            'post_shares': get_action_value(actions, 'post_share'),
            'post_engagement': get_action_value(actions, 'post_engagement'),
            'page_likes': get_action_value(actions, 'like'),
            
            'amount_spent': insights_data.get('spend')
        }
        results.append(result)
    
    return {
        'data': results,
        'summary': {
            'total_ads': len(results),
            'date_preset': date_preset,
            'time_range': time_range,
            'account_id': act_id,
            'campaign_id': campaign_id,
            'min_spend_filter': min_spend
        }
    }


# =============================================================================
# PAGINATION HELPER
# =============================================================================

@mcp.tool()
def fetch_pagination_url(url: str) -> Dict:
    """
    Fetch data from a pagination URL.
    Used when results have 'paging.next' or 'paging.previous' URLs.
    
    Args:
        url: Full pagination URL from a previous API response
    
    Returns:
        Dict: JSON response with next/previous page of data
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            if 'error' in error_data:
                error_msg = error_data['error'].get('message', str(e))
                raise requests.HTTPError(f"Facebook API Error: {error_msg}", response=e.response)
        except (ValueError, KeyError):
            pass
        raise
    except requests.exceptions.Timeout:
        raise requests.RequestException("Request to pagination URL timed out after 30 seconds")
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"Network error fetching pagination URL: {str(e)}")


# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Facebook Ads MCP Server')
    parser.add_argument('--fb-token', type=str, help='Facebook access token')
    parser.add_argument('--transport', type=str, choices=['stdio', 'sse'], default='stdio',
                       help='Transport mode: stdio (local) or sse (remote)')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port for SSE server (default: 8000)')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                       help='Host for SSE server (default: 0.0.0.0)')
    
    args = parser.parse_args()
    
    # Validate token is available (from env or args)
    try:
        _get_fb_access_token()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Run with appropriate transport
    if args.transport == 'sse':
        print(f"🚀 Starting Facebook Ads MCP Server in SSE mode on {args.host}:{args.port}")
        print(f"📡 Connect your Claude Desktop to: http://{args.host}:{args.port}/sse")
        mcp.run(transport='sse', host=args.host, port=args.port)
    else:
        # Default stdio mode for local use
        mcp.run()



# =============================================================================
# LIGHTWEIGHT SUMMARY REPORT
# =============================================================================

@mcp.tool()
def get_summary_report(
    act_id: str,
    date_preset: Optional[str] = "last_30d",
    time_range: Optional[Dict[str, str]] = None,
    limit: Optional[int] = 50
) -> Dict:
    """
    Get a lightweight summary report with only key metrics (no detailed fields).
    
    Perfect for quick overviews without hitting context limits.
    Returns only essential metrics per ad:
    - IDs and names
    - Spend, impressions, clicks
    - CTR, CPC, CPM
    - Conversions and CPA
    
    Args:
        act_id: Account ID (format: act_1234567890)
        date_preset: Date range preset (default: 'last_30d')
        time_range: Custom date range (e.g., {"since":"2024-01-01","until":"2024-01-31"})
        limit: Max number of ads to retrieve (default: 50, max: 100)
    
    Returns:
        Dict: Lightweight summary with only key performance metrics
    """
    access_token = _get_fb_access_token()
    
    # Get insights at account level with ad breakdown
    insights_url = f"{FB_GRAPH_URL}/{act_id}/insights"
    
    insights_params = {
        'access_token': access_token,
        'level': 'ad',
        'fields': 'ad_id,ad_name,campaign_id,campaign_name,adset_id,adset_name,spend,impressions,clicks,ctr,cpc,cpm,actions,cost_per_action_type',
        'limit': limit,
        'filtering': json.dumps([{
            'field': 'spend',
            'operator': 'GREATER_THAN',
            'value': 0
        }])
    }
    
    if time_range:
        insights_params['time_range'] = json.dumps(time_range)
    elif date_preset:
        insights_params['date_preset'] = date_preset
    
    try:
        insights_response = _make_graph_api_call(insights_url, insights_params)
        ads_data = insights_response.get('data', [])
    except Exception as e:
        return {
            'error': f"Failed to fetch insights: {str(e)}",
            'date_range': f"{date_preset or time_range}"
        }
    
    # Helper to extract conversion data
    def get_conversions(actions, action_type='purchase'):
        if not actions:
            return 0
        for action in actions:
            if action_type in action.get('action_type', ''):
                return int(float(action.get('value', 0)))
        return 0
    
    # Helper to get CPA
    def get_cpa(cost_per_actions, action_type='purchase'):
        if not cost_per_actions:
            return None
        for action in cost_per_actions:
            if action_type in action.get('action_type', ''):
                return float(action.get('value', 0))
        return None
    
    # Build summary results
    results = []
    total_spend = 0
    total_conversions = 0
    
    for ad in ads_data:
        spend = float(ad.get('spend', 0))
        conversions = get_conversions(ad.get('actions', []))
        cpa = get_cpa(ad.get('cost_per_action_type', []))
        
        total_spend += spend
        total_conversions += conversions
        
        results.append({
            'ad_id': ad.get('ad_id'),
            'ad_name': ad.get('ad_name'),
            'campaign_id': ad.get('campaign_id'),
            'campaign_name': ad.get('campaign_name'),
            'adset_id': ad.get('adset_id'),
            'adset_name': ad.get('adset_name'),
            'spend': round(spend, 2),
            'impressions': int(ad.get('impressions', 0)),
            'clicks': int(ad.get('clicks', 0)),
            'ctr': float(ad.get('ctr', 0)),
            'cpc': float(ad.get('cpc', 0)),
            'cpm': float(ad.get('cpm', 0)),
            'conversions': conversions,
            'cpa': round(cpa, 2) if cpa else None
        })
    
    return {
        'data': results,
        'summary': {
            'total_ads': len(results),
            'total_spend': round(total_spend, 2),
            'total_conversions': total_conversions,
            'average_cpa': round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
            'date_preset': date_preset,
            'time_range': time_range,
            'account_id': act_id
        }
    }
