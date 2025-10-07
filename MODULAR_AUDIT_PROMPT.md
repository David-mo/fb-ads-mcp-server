# MODULAR META ADS AUDIT - CONTEXT-EFFICIENT APPROACH

This audit is broken into small, independent modules that won't hit context limits.
Run each module separately, then combine insights.

---

## MODULE 1: ACCOUNT SNAPSHOT (5 mins)

**Copy and paste this into Claude Desktop:**

```
Please provide a quick account snapshot for act_994348650619937:

1. List all my ad accounts
2. Get account details: name, status, balance, currency, total amount_spent
3. Get all campaigns with fields: name, objective, status, effective_status, daily_budget
4. Summarize:
   - Total campaigns: X
   - Active campaigns: X
   - Campaign objectives breakdown
   - Total daily budget allocated
```

**Expected output:** 1-2 page summary

---

## MODULE 2: TOP PERFORMERS ANALYSIS (5 mins)

**Copy and paste this into Claude Desktop:**

```
Analyze top performers for act_994348650619937 (last 30 days):

1. Get summary report for last 30 days (limit: 50)
2. Identify:
   - Top 5 campaigns by lowest CPA
   - Top 5 campaigns by highest conversion volume
   - Top 5 ads by highest CTR
3. For each top performer, show:
   - Name, spend, conversions, CPA
   - What makes it successful?
4. Calculate:
   - % of total spend going to top 20% performers
   - Average CPA of top performers vs. account average
```

**Expected output:** Table + analysis

---

## MODULE 3: UNDERPERFORMERS & WASTE (5 mins)

**Copy and paste this into Claude Desktop:**

```
Identify underperformers and wasted spend for act_994348650619937 (last 30 days):

1. Get summary report for last 30 days
2. Find:
   - Campaigns with CPA >$50 (or your threshold)
   - Ads with >$100 spend but 0 conversions
   - Campaigns with CTR <0.5%
3. Calculate total wasted spend
4. Recommend:
   - What to pause immediately
   - Potential savings per day
```

**Expected output:** List of problem areas with $ impact

---

## MODULE 4: BUDGET ALLOCATION REVIEW (5 mins)

**Copy and paste this into Claude Desktop:**

```
Review budget allocation for act_994348650619937:

1. Get campaigns with fields: name, daily_budget, lifetime_budget, effective_status
2. Get campaign insights for each active campaign (last 30 days): spend, conversions, CPA
3. Analyze:
   - Budget distribution by campaign
   - Performance vs. budget allocation
   - Which high-performers are budget-constrained?
   - Which low-performers are over-funded?
4. Recommend:
   - 3 budget reallocation opportunities
   - Expected impact of each change
```

**Expected output:** Budget reallocation plan

---

## MODULE 5: CREATIVE PERFORMANCE (5 mins)

**Copy and paste this into Claude Desktop:**

```
Analyze creative performance for act_994348650619937 (last 30 days):

1. Get summary report (limit: 100)
2. Count:
   - Video ads vs. static vs. carousel
   - Ads by creative format
3. Calculate average metrics by format:
   - CTR by format
   - Conversion rate by format
   - CPA by format
4. Identify:
   - Top 3 winning creative patterns
   - Ads with high frequency (>4) indicating fatigue
   - Creatives that should be refreshed
```

**Expected output:** Creative insights + refresh recommendations

---

## MODULE 6: WEEKLY TREND COMPARISON (5 mins)

**Copy and paste this into Claude Desktop:**

```
Compare performance trends for act_994348650619937:

1. Get summary report for last 7 days
2. Get summary report for previous 7 days (use time_range)
3. Compare:
   - Week-over-week spend change
   - Week-over-week conversion change
   - Week-over-week CPA change
4. Identify:
   - Campaigns improving
   - Campaigns declining
   - Emerging winners/losers
```

**Expected output:** Trend analysis with % changes

---

## MODULE 7: SPECIFIC CAMPAIGN DEEP DIVE (5 mins)

**Copy and paste this into Claude Desktop:**

```
Deep dive into [CAMPAIGN_NAME] for act_994348650619937:

1. Get campaign details and insights (last 30 days)
2. Get all ad sets in this campaign
3. Get ad set insights for each ad set
4. Get all ads in this campaign
5. Analyze:
   - Campaign structure quality
   - Ad set performance distribution
   - Top/bottom performing ads
   - Targeting effectiveness
6. Recommend specific optimizations for this campaign
```

**Expected output:** Campaign-specific action plan

---

## MODULE 8: CONVERSION FUNNEL ANALYSIS (5 mins)

**Copy and paste this into Claude Desktop:**

```
Analyze the conversion funnel for act_994348650619937 (last 30 days):

1. Get summary report with all action fields
2. Map the funnel:
   - Impressions → Clicks (CTR)
   - Clicks → Landing Page Views
   - Landing Page Views → Add to Cart
   - Add to Cart → Checkout Initiated
   - Checkout Initiated → Purchase
3. Calculate conversion rates at each stage
4. Identify:
   - Biggest drop-off points
   - Campaigns with funnel issues
   - Optimization opportunities
```

**Expected output:** Funnel visualization + bottleneck fixes

---

## MODULE 9: AUDIENCE TARGETING INSIGHTS (5 mins)

**Copy and paste this into Claude Desktop:**

```
Analyze audience targeting for act_994348650619937:

1. Get campaigns with best CPA (top 5)
2. For each, get ad sets with targeting details
3. Identify patterns:
   - Common targeting elements in winners
   - Broad vs. specific targeting performance
   - Geographic targeting effectiveness
4. Recommend:
   - Targeting strategies to expand
   - Audiences to test
   - Targeting to narrow/eliminate
```

**Expected output:** Targeting playbook

---

## MODULE 10: EXECUTIVE SUMMARY (10 mins)

**After completing modules 1-9, copy and paste this:**

```
Based on the previous analysis modules, create an executive summary:

### ACCOUNT HEALTH SCORE: [X/100]

Consider:
- Account structure quality
- Budget allocation efficiency
- Creative performance
- Conversion funnel health
- Performance trends

### KEY METRICS (Last 30 Days):
- Total Spend
- Total Conversions
- Average CPA
- Average CTR, CPC, CPM

### TOP 3 QUICK WINS:
1. [Specific action with $ impact]
2. [Specific action with $ impact]
3. [Specific action with $ impact]

### TOP 3 STRATEGIC OPPORTUNITIES:
1. [Long-term improvement with impact]
2. [Long-term improvement with impact]
3. [Long-term improvement with impact]

### CRITICAL ISSUES:
[Anything requiring immediate attention]

### IMPLEMENTATION PRIORITY:
Week 1: [Actions]
Week 2-4: [Actions]
Month 2-3: [Actions]

### EXPECTED IMPACT:
- CPA reduction: X%
- Conversion increase: X%
- Monthly savings: $X
```

**Expected output:** Complete executive summary

---

## USAGE TIPS

### Strategy 1: Focus Audit (30 mins)
Run modules in this order:
1. Account Snapshot
2. Top Performers
3. Underperformers
4. Executive Summary

### Strategy 2: Deep Dive (60 mins)
Run all 10 modules sequentially, save each output

### Strategy 3: Weekly Check-in (15 mins)
Run only:
1. Account Snapshot
2. Weekly Trend Comparison
3. Quick wins summary

### Strategy 4: Campaign-Specific (20 mins)
Run:
1. Specific Campaign Deep Dive (for each campaign of interest)
2. Creative Performance
3. Audience Targeting

---

## SAVING OUTPUTS

After each module, either:
- **Copy to a doc** for later reference
- **Ask Claude to summarize** key findings in 3-5 bullets
- **Create action items** immediately

This keeps context manageable!

---

## COMBINING INSIGHTS

At the end, you can ask:

```
Based on all the module outputs I've shared, what are the top 5 
priority actions I should take this week, ranked by expected impact?
```

This works even if the original data is out of context!

