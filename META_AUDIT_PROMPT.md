# META ADS ACCOUNT AUDIT - COMPREHENSIVE ANALYSIS PROMPT

Use this prompt to conduct a thorough audit of a Meta Ads account using the Facebook Ads MCP Server.

---

## AUDIT SCOPE & OBJECTIVES

I need you to conduct a comprehensive Meta Ads account audit for **[ACCOUNT_ID]** covering the period from **[START_DATE]** to **[END_DATE]**.

The audit should identify:
- Performance trends and anomalies
- Budget allocation efficiency
- Creative performance
- Campaign structure optimization opportunities
- Audience targeting insights
- Conversion funnel analysis
- Recommendations for improvement

---

## STEP 1: ACCOUNT OVERVIEW & HEALTH CHECK

**Objective:** Get a high-level view of the account structure and status

1. **List all ad accounts** linked to this token to confirm access
   - Use: `list_ad_accounts()`
   
2. **Get account details** for the primary account
   - Use: `get_details_of_ad_account(act_id="act_XXXXXX", fields=["name", "account_status", "amount_spent", "balance", "currency", "spend_cap", "timezone_name"])`
   
3. **Document:**
   - Account name and ID
   - Current balance and spend cap
   - Account status and any restrictions
   - Total amount spent in the audit period

---

## STEP 2: CAMPAIGN STRUCTURE ANALYSIS

**Objective:** Understand the campaign architecture and organization

1. **Retrieve all campaigns** in the account
   - Use: `get_campaigns_by_adaccount(act_id="act_XXXXXX", fields=["name", "objective", "status", "effective_status", "daily_budget", "lifetime_budget", "created_time", "updated_time", "start_time", "stop_time"], limit=100)`

2. **Analyze and document:**
   - Total number of campaigns
   - Campaign objectives breakdown (how many per objective)
   - Status distribution (Active, Paused, Archived)
   - Budget structure (CBO vs ABO)
   - Naming convention consistency
   - Campaign organization patterns

3. **Identify issues:**
   - Duplicate or redundant campaigns
   - Campaigns with unclear objectives
   - Old campaigns that should be archived
   - Budget allocation imbalances

---

## STEP 3: PERFORMANCE METRICS - LAST 30 DAYS

**Objective:** Analyze overall account performance and identify top performers/underperformers

1. **Get comprehensive ad report** for the last 30 days
   - Use: `get_comprehensive_ad_report(act_id="act_XXXXXX", date_preset="last_30d", limit=100)`

2. **For each campaign with spend**, get detailed insights:
   - Use: `get_campaign_insights(campaign_id="CAMPAIGN_ID", fields=["impressions", "clicks", "spend", "cpc", "cpm", "ctr", "reach", "frequency", "actions", "action_values", "cost_per_action_type", "purchase", "cost_per_purchase"], date_preset="last_30d")`

3. **Analyze and calculate:**
   - **Overall Account Metrics:**
     - Total spend
     - Total impressions
     - Total clicks
     - Overall CTR
     - Average CPC
     - Average CPM
     - Total conversions/purchases
     - Overall CPA/Cost per purchase
     - ROAS (if revenue data available)

   - **Top Performers (Top 10):**
     - Campaigns by ROAS
     - Campaigns by conversion volume
     - Campaigns by CTR
     - Ads by engagement
     - Ads by conversion rate

   - **Underperformers (Bottom 10):**
     - Campaigns with highest CPA
     - Campaigns with lowest CTR
     - Ads with no conversions despite spend
     - Campaigns exceeding target CPA by >50%

4. **Document performance distribution:**
   - What % of spend is going to top 20% performers?
   - What % of conversions come from top 20% campaigns?
   - Pareto analysis (80/20 rule application)

---

## STEP 4: CREATIVE PERFORMANCE ANALYSIS

**Objective:** Evaluate ad creative effectiveness and identify winning patterns

1. **Analyze creative types:**
   - Count of video ads vs. static images vs. carousels
   - Performance breakdown by creative format
   - Asset URL analysis for creative diversity

2. **Identify creative winners:**
   - Top 20 ads by:
     - CTR
     - Conversion rate
     - Cost per conversion
     - Engagement rate (reactions + comments + shares)
     - Video completion rate (for video ads)

3. **Creative fatigue analysis:**
   - Ads running >60 days
   - Performance degradation over time
   - Frequency analysis (ads with frequency >3)

4. **Document patterns:**
   - Common elements in top performers
   - Creative themes that resonate
   - Messaging angles that work
   - Format preferences by audience

---

## STEP 5: AUDIENCE & TARGETING ANALYSIS

**Objective:** Evaluate targeting strategy and audience performance

1. **For top-performing ad sets**, retrieve targeting details:
   - Use: `get_adsets_by_campaign(campaign_id="CAMPAIGN_ID", fields=["name", "targeting", "optimization_goal", "billing_event", "daily_budget", "lifetime_budget", "effective_status"])`

2. **Analyze targeting patterns:**
   - Broad vs. specific targeting
   - Lookalike audiences usage
   - Interest-based targeting effectiveness
   - Geographic targeting distribution
   - Age and gender targeting patterns

3. **Document:**
   - Which targeting strategies drive best CPA?
   - Audience overlap issues
   - Untapped audience opportunities
   - Targeting redundancies

---

## STEP 6: BUDGET ALLOCATION & PACING

**Objective:** Assess if budget is being allocated efficiently

1. **Calculate budget distribution:**
   - % of budget by campaign objective
   - % of budget by funnel stage (TOF, MOF, BOF)
   - Daily spend trends over the audit period
   - Budget pacing vs. goals

2. **Identify allocation issues:**
   - Campaigns overspending with poor ROAS
   - High-performing campaigns constrained by budget
   - Budget sitting idle in paused campaigns
   - Recommended reallocation opportunities

3. **Document:**
   - Is budget weighted toward winners?
   - Are there quick wins by budget reallocation?
   - Recommended daily budget changes by campaign

---

## STEP 7: CONVERSION FUNNEL ANALYSIS

**Objective:** Understand the customer journey and conversion efficiency

1. **Map the funnel:**
   - Impressions → Clicks (CTR)
   - Clicks → Landing Page Views (LP CTR)
   - Landing Page Views → Add to Cart
   - Add to Cart → Checkout Initiated
   - Checkout Initiated → Purchase

2. **Calculate conversion rates at each stage:**
   - Where is the biggest drop-off?
   - Which campaigns have the best funnel efficiency?
   - Which campaigns have funnel issues?

3. **Analyze action metrics:**
   - Cost per landing page view
   - Cost per add to cart
   - Cost per checkout initiated
   - Cost per purchase
   - Cart abandonment rate

4. **Document:**
   - Funnel bottlenecks
   - Optimization opportunities
   - Campaigns that drive awareness but don't convert
   - Campaigns that convert well but lack volume

---

## STEP 8: TIME-BASED PERFORMANCE ANALYSIS

**Objective:** Identify trends and seasonality patterns

1. **Compare performance across time periods:**
   - Last 7 days vs. previous 7 days
   - Last 30 days vs. previous 30 days
   - Week-over-week trends
   - Day-of-week performance patterns

2. **Use time_range parameter for custom periods:**
   - Use: `get_comprehensive_ad_report(act_id="act_XXXXXX", time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"})`

3. **Document:**
   - Performance trends (improving/declining)
   - Best performing days/times
   - Seasonal patterns
   - Anomalies or sudden changes

---

## STEP 9: AD SET & PLACEMENT ANALYSIS

**Objective:** Evaluate ad set structure and placement effectiveness

1. **For key campaigns, analyze ad sets:**
   - Use: `get_adsets_by_campaign(campaign_id="CAMPAIGN_ID", fields=["name", "targeting", "optimization_goal", "bid_strategy", "daily_budget", "effective_status"])`

2. **Get ad set insights:**
   - Use: `get_adset_insights(adset_id="ADSET_ID", fields=["impressions", "clicks", "spend", "cpc", "ctr", "actions", "cost_per_action_type"], date_preset="last_30d")`

3. **Analyze:**
   - Ad set organization and structure
   - Single ad set vs. multiple ad set strategies
   - Bid strategy effectiveness
   - Placement performance (if data available)

4. **Document:**
   - Ad set best practices compliance
   - Optimization opportunities
   - Testing framework effectiveness
   - Placement recommendations

---

## STEP 10: CREATIVE TESTING & ITERATION

**Objective:** Assess testing methodology and creative refresh cadence

1. **Identify active tests:**
   - Campaigns/ad sets with multiple active creatives
   - A/B test setups
   - Creative rotation strategies

2. **Evaluate testing rigor:**
   - Are tests properly structured?
   - Sufficient budget allocated to tests?
   - Clear winners emerging?
   - Test duration and statistical significance

3. **Creative refresh analysis:**
   - When were creatives last updated?
   - Ad sets running same creative >90 days
   - Creative iteration velocity

4. **Document:**
   - Testing best practices compliance
   - Recommended test structure improvements
   - Creative refresh schedule recommendations
   - Quick win opportunities from test results

---

## STEP 11: CAMPAIGN NAMING & ORGANIZATION AUDIT

**Objective:** Evaluate naming conventions and account organization

1. **Analyze naming patterns:**
   - Consistency across campaigns
   - Use of naming conventions
   - Clarity and descriptiveness
   - UTM parameter usage

2. **Organizational structure:**
   - Campaign grouping logic
   - Ad set organization within campaigns
   - Ad organization within ad sets
   - Use of labels or tags (if available)

3. **Document:**
   - Naming convention issues
   - Recommended naming structure
   - Organizational improvements
   - Easier reporting setup opportunities

---

## STEP 12: COMPETITIVE & BENCHMARK ANALYSIS

**Objective:** Compare performance against industry benchmarks

1. **Calculate key benchmarks:**
   - CTR by objective
   - CPC by objective
   - CPM by industry
   - Conversion rate by funnel stage
   - CPA by objective

2. **Compare to industry standards:**
   - Is CTR above/below industry average?
   - Is CPC competitive?
   - How does conversion rate compare?

3. **Document:**
   - Metrics above benchmark (strengths)
   - Metrics below benchmark (opportunities)
   - Competitive positioning
   - Performance gaps to close

---

## STEP 13: RECOMMENDATIONS & ACTION PLAN

**Objective:** Provide prioritized, actionable recommendations

### IMMEDIATE ACTIONS (Week 1):
1. **Quick Wins:**
   - Pause campaigns/ads with CPA >200% of target
   - Increase budget on top performers by X%
   - Turn off creative fatigue ads (frequency >5)
   - Archive old inactive campaigns

2. **Priority Optimizations:**
   - [Specific recommendations based on findings]

### SHORT-TERM ACTIONS (Weeks 2-4):
1. **Creative Refresh:**
   - Launch new creatives based on winner patterns
   - Retire underperforming creatives
   - Set up creative testing framework

2. **Targeting Optimization:**
   - Test new audience segments
   - Refine underperforming audiences
   - Address audience overlap

3. **Budget Reallocation:**
   - Shift $X from Campaign A to Campaign B
   - Implement daily budget caps on high-CPA campaigns

### MEDIUM-TERM ACTIONS (Months 2-3):
1. **Structural Improvements:**
   - Implement proper naming conventions
   - Reorganize campaign structure
   - Set up proper testing framework

2. **Strategic Initiatives:**
   - Launch new campaign objectives
   - Expand to new markets/audiences
   - Implement advanced measurement

### KPIs TO TRACK:
- Overall account CPA target: $X
- Minimum ROAS: X:1
- Target CTR: X%
- Maximum frequency: X
- Monthly spend target: $X
- Monthly conversion target: X

---

## STEP 14: EXECUTIVE SUMMARY

**Objective:** Create a clear, concise summary for stakeholders

Format the final output as:

### ACCOUNT HEALTH SCORE: [X/100]

**Overall Assessment:** [2-3 sentences on account health]

### KEY METRICS (Last 30 Days):
- Total Spend: $X
- Total Conversions: X
- Average CPA: $X
- Average CTR: X%
- Average CPC: $X
- Average CPM: $X
- ROAS: X:1

### TOP 3 STRENGTHS:
1. [Specific strength with data]
2. [Specific strength with data]
3. [Specific strength with data]

### TOP 3 OPPORTUNITIES:
1. [Specific opportunity with potential impact]
2. [Specific opportunity with potential impact]
3. [Specific opportunity with potential impact]

### CRITICAL ISSUES:
- [Any urgent problems requiring immediate attention]

### ESTIMATED IMPACT OF RECOMMENDATIONS:
- Expected CPA reduction: X%
- Expected conversion increase: X%
- Expected ROAS improvement: X%
- Timeline to impact: X weeks

---

## AUDIT COMPLETION CHECKLIST

- [ ] All campaigns analyzed
- [ ] Performance data validated
- [ ] Creative patterns identified
- [ ] Audience insights documented
- [ ] Budget allocation reviewed
- [ ] Funnel analysis completed
- [ ] Benchmarks compared
- [ ] Recommendations prioritized
- [ ] Action plan created
- [ ] Executive summary written
- [ ] Supporting data compiled

---

## NOTES FOR EFFECTIVE AUDIT:

1. **Be Data-Driven:** Every recommendation should be backed by specific data points
2. **Be Specific:** Avoid generic advice; provide exact campaign IDs, budget amounts, etc.
3. **Prioritize Impact:** Focus on changes that will move the needle most
4. **Consider Resources:** Recommendations should be implementable with available resources
5. **Set Expectations:** Be clear about expected outcomes and timelines
6. **Follow Up:** Plan for post-implementation review in 30 days

---

**Audit conducted on:** [DATE]
**Audit period:** [START_DATE] to [END_DATE]
**Account:** [ACCOUNT_NAME] (act_XXXXXX)
**Auditor:** [NAME/TEAM]

