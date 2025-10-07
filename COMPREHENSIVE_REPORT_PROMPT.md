# COMPREHENSIVE AD REPORT - READY-TO-USE PROMPTS

Use these prompts in Claude Desktop to pull complete ad data with all metrics.

---

## BASIC: All Ads with Spend (Last 30 Days)

```
Get comprehensive ad report for account act_994348650619937 for the last 30 days
```

Returns ALL ads that have spend in the last 30 days with full metrics.

---

## FILTERED: Ads with Minimum Spend Threshold

```
Get comprehensive ad report for account act_994348650619937 for the last 30 days with minimum spend of 100
```

Only returns ads that spent at least $100 in the last 30 days.

**Common thresholds:**
- `min_spend=10` - Ads with at least $10 spend
- `min_spend=50` - Ads with at least $50 spend  
- `min_spend=100` - Ads with at least $100 spend
- `min_spend=500` - Ads with at least $500 spend

---

## CUSTOM DATE RANGE: Specific Time Period

```
Get comprehensive ad report for account act_994348650619937 with time range from 2024-10-01 to 2024-10-07 and minimum spend of 50
```

Pulls ads with at least $50 spend between October 1-7, 2024.

---

## LAST 7 DAYS: Recent Performance

```
Get comprehensive ad report for account act_994348650619937 for last 7 days
```

All ads with spend in the last week.

---

## CAMPAIGN-SPECIFIC: Single Campaign Analysis

```
Get comprehensive ad report for campaign 6770765233220 for last 30 days
```

Only ads within a specific campaign.

---

## FIELD MAPPING

The report returns these exact fields matching your requirements:

| Your Field Name | API Field Name |
|----------------|----------------|
| Ad Creative ID | `ad_creative_id` |
| Ad ID | `ad_id` |
| Ad Name | `ad_name` |
| Campaign ID | `campaign_id` |
| Campaign Name | `campaign_name` |
| Ad Set ID | `ad_set_id` |
| Ad Set name | `ad_set_name` |
| Ad Status | `ad_status` |
| Delivery | `delivery` |
| Asset URL | `asset_url` |
| Reach | `reach` |
| Impressions | `impressions` |
| Frequency | `frequency` |
| Purchases | `purchases` (flexible - auto-detects conversion event) |
| Cost Per Purchases | `cost_per_purchase` (flexible - matches conversion event) |
| Clicks (All) | `clicks_all` |
| Unique Clicks (All) | `unique_clicks_all` |
| CTR (All) | `ctr_all` |
| Unique CTR (All) | `unique_ctr_all` |
| CPC (All) | `cpc_all` |
| CPM (Cost per 1,000 Impressions) | `cpm` |
| 3-second video plays | `video_3_sec_plays` |
| Video Plays at 25 percent | `video_plays_25_percent` |
| Video Plays at 50 percent | `video_plays_50_percent` |
| Video Plays at 75 percent | `video_plays_75_percent` |
| Video Plays at 100 percent | `video_plays_100_percent` |
| Video Plays | `video_plays` |
| ThruPlays | `thru_plays` |
| Adds To Cart | `adds_to_cart` |
| Content Views | `content_views` |
| Checkouts Initiated | `checkouts_initiated` |
| Landing Page Views | `landing_page_views` |
| Link Clicks | `link_clicks` |
| Outbound Clicks | `outbound_clicks` |
| Post Reactions | `post_reactions` |
| Post Comments | `post_comments` |
| Post Saves | `post_saves` |
| Post Shares | `post_shares` |
| Post Engagement | `post_engagement` |
| Page Likes | `page_likes` |
| Amount Spent | `amount_spent` |

---

## FLEXIBLE CONVERSION TRACKING

The function automatically detects your account's conversion events in this order:

1. **Purchase** - Standard e-commerce purchase
2. **Offsite Conversion (Purchase)** - Pixel-based purchase tracking
3. **Offsite Conversion (Generic)** - Any offsite conversion
4. **Onsite Conversion** - On-platform conversions

Cost per purchase follows the same logic - it will match whatever conversion event is being tracked.

---

## EXPORT TO CSV/EXCEL

After running the report, you can ask:

```
Format this data as a CSV table
```

or

```
Show me this in a table format that I can copy to Excel
```

---

## TIPS

1. **Start with higher min_spend** - Use `min_spend=50` or `min_spend=100` to reduce data volume
2. **Use shorter date ranges** - `last_7d` instead of `last_30d` for faster results
3. **Filter by campaign** - Analyze one campaign at a time for detailed insights
4. **Batch exports** - Request small batches (limit=25) if context window is an issue

---

## EXAMPLE WORKFLOW

**Step 1: Get overview**
```
Get comprehensive ad report for account act_994348650619937 for last 7 days with minimum spend of 100
```

**Step 2: Ask for analysis**
```
Show me the top 10 ads by CTR and bottom 10 by cost per purchase
```

**Step 3: Export**
```
Format the full report as a CSV table I can copy to Excel
```

---

**Ready to use! Just copy any prompt above and paste into Claude Desktop.** 🚀
