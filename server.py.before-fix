"""
Facebook Ads MCP Server

A Model Context Protocol server that connects AI assistants to Facebook's Ads API.
Enables natural language queries to fetch campaign data, insights, and ad performance metrics.
"""

from mcp.server.fastmcp import FastMCP
import requests
from typing import Dict, List, Optional, Any
import sys
import json

# Constants
FB_API_VERSION = "v22.0"
FB_GRAPH_URL = f"https://graph.facebook.com/{FB_API_VERSION}"

# Initialize MCP server
mcp = FastMCP("fb-ads-mcp-server")

# Global token storage
FB_ACCESS_TOKEN = None


def _get_fb_access_token() -> str:
    """
    Get Facebook access token from command line arguments.
    Cache in memory after first read.
    
    Expects: python server.py --fb-token YOUR_TOKEN
    
    Returns:
        str: Facebook access token
        
    Raises:
        ValueError: If token is not provided via command line arguments
    """
    global FB_ACCESS_TOKEN
    
    if FB_ACCESS_TOKEN is None:
        # Parse --fb-token from sys.argv
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
                "Please run with: python server.py --fb-token YOUR_TOKEN"
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
    limit: Optional[int] = 100
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
    - Purchases, Cost Per Purchase
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
    
    Returns:
        Dict: Comprehensive ad report with all requested fields
        
    Example:
        To get all ads from an account for the last 30 days:
        get_comprehensive_ad_report("act_123456789")
        
        To get ads from a specific campaign:
        get_comprehensive_ad_report("act_123456789", campaign_id="6770765233220")
    """
    access_token = _get_fb_access_token()
    
    # Determine the base URL - either all ads in account or ads in specific campaign
    if campaign_id:
        url = f"{FB_GRAPH_URL}/{campaign_id}/ads"
    else:
        url = f"{FB_GRAPH_URL}/{act_id}/ads"
    
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
        'reach',
        'impressions',
        'frequency',
        'spend',
        'purchase',
        'cost_per_purchase',
        'clicks',
        'unique_clicks',
        'ctr',
        'unique_ctr',
        'cpc',
        'cpm',
        'video_play_actions',
        'video_thruplay_watched_actions',
        'video_p25_watched_actions',
        'video_p50_watched_actions',
        'video_p75_watched_actions',
        'video_p100_watched_actions',
        'video_continuous_2_sec_watched_actions',
        'actions',
        'action_values'
    ]
    
    params = {
        'access_token': access_token,
        'fields': ','.join(ad_fields),
        'limit': limit
    }
    
    # Get ads data
    ads_response = _make_graph_api_call(url, params)
    
    # Now fetch insights for each ad
    results = []
    if 'data' in ads_response:
        for ad in ads_response['data']:
            ad_id = ad.get('id')
            
            # Get insights for this ad
            insights_url = f"{FB_GRAPH_URL}/{ad_id}/insights"
            insights_params = {
                'access_token': access_token,
                'fields': ','.join(insight_fields)
            }
            
            if time_range:
                insights_params['time_range'] = json.dumps(time_range)
            elif date_preset:
                insights_params['date_preset'] = date_preset
            
            try:
                insights_response = _make_graph_api_call(insights_url, insights_params)
                insights_data = insights_response.get('data', [{}])[0] if insights_response.get('data') else {}
            except Exception as e:
                insights_data = {'error': str(e)}
            
            # Extract asset URL from creative
            asset_url = None
            creative = ad.get('creative', {})
            if creative:
                # Try to get video URL or image URL
                asset_url = creative.get('thumbnail_url') or creative.get('image_url')
                
                # Check object_story_spec for video
                if not asset_url and creative.get('object_story_spec'):
                    video_data = creative.get('object_story_spec', {}).get('video_data', {})
                    if video_data:
                        asset_url = f"Video ID: {video_data.get('video_id', 'N/A')}"
            
            # Helper function to extract action values
            def get_action_value(actions_list, action_type):
                if not actions_list:
                    return None
                for action in actions_list:
                    if action.get('action_type') == action_type:
                        return action.get('value')
                return None
            
            # Extract all actions
            actions = insights_data.get('actions', [])
            video_actions = insights_data.get('video_play_actions', [])
            
            # Build comprehensive result
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
                
                # Performance metrics
                'reach': insights_data.get('reach'),
                'impressions': insights_data.get('impressions'),
                'frequency': insights_data.get('frequency'),
                'purchases': get_action_value(actions, 'purchase') or get_action_value(actions, 'offsite_conversion.fb_pixel_purchase'),
                'cost_per_purchase': insights_data.get('cost_per_purchase'),
                'clicks_all': insights_data.get('clicks'),
                'unique_clicks_all': insights_data.get('unique_clicks'),
                'ctr_all': insights_data.get('ctr'),
                'unique_ctr_all': insights_data.get('unique_ctr'),
                'cpc_all': insights_data.get('cpc'),
                'cpm': insights_data.get('cpm'),
                
                # Video metrics
                'video_3_sec_plays': get_action_value(insights_data.get('video_continuous_2_sec_watched_actions', []), 'video_view'),
                'video_plays_25_percent': get_action_value(insights_data.get('video_p25_watched_actions', []), 'video_view'),
                'video_plays_50_percent': get_action_value(insights_data.get('video_p50_watched_actions', []), 'video_view'),
                'video_plays_75_percent': get_action_value(insights_data.get('video_p75_watched_actions', []), 'video_view'),
                'video_plays_100_percent': get_action_value(insights_data.get('video_p100_watched_actions', []), 'video_view'),
                'video_plays': get_action_value(video_actions, 'video_view'),
                'thru_plays': get_action_value(insights_data.get('video_thruplay_watched_actions', []), 'video_view'),
                
                # Conversion actions
                'adds_to_cart': get_action_value(actions, 'add_to_cart') or get_action_value(actions, 'offsite_conversion.fb_pixel_add_to_cart'),
                'content_views': get_action_value(actions, 'view_content') or get_action_value(actions, 'offsite_conversion.fb_pixel_view_content'),
                'checkouts_initiated': get_action_value(actions, 'initiate_checkout') or get_action_value(actions, 'offsite_conversion.fb_pixel_initiate_checkout'),
                'landing_page_views': get_action_value(actions, 'landing_page_view'),
                'link_clicks': get_action_value(actions, 'link_click'),
                'outbound_clicks': get_action_value(actions, 'outbound_click'),
                
                # Engagement metrics
                'post_reactions': get_action_value(actions, 'post_reaction'),
                'post_comments': get_action_value(actions, 'comment'),
                'post_saves': get_action_value(actions, 'post_save'),
                'post_shares': get_action_value(actions, 'post_share'),
                'post_engagement': get_action_value(actions, 'post_engagement'),
                'page_likes': get_action_value(actions, 'like'),
                
                # Spend
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
            'campaign_id': campaign_id
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
    # FastMCP will handle the MCP protocol
    mcp.run()

