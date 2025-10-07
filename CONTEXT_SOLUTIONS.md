# CONTEXT WINDOW SOLUTIONS - QUICK REFERENCE

## Problem
Claude Desktop hits context window limits when running comprehensive audits due to large API responses (100+ ads × 40+ fields).

---

## ✅ SOLUTION 1: Use the Modular Audit Approach

**File:** `MODULAR_AUDIT_PROMPT.md`

Break your audit into 10 small, independent modules:
1. Account Snapshot (5 mins)
2. Top Performers (5 mins)  
3. Underperformers (5 mins)
4. Budget Allocation (5 mins)
5. Creative Performance (5 mins)
6. Weekly Trends (5 mins)
7. Campaign Deep Dive (5 mins)
8. Conversion Funnel (5 mins)
9. Audience Targeting (5 mins)
10. Executive Summary (10 mins)

**Benefit:** Each module stays within context limits, you can run them separately and combine insights later.

**Best For:** Deep analysis without hitting limits

---

## ✅ SOLUTION 2: Use the Lightweight Summary Tool

**Tool:** `get_summary_report()`

Use the lightweight summary tool:
```
Get summary report for act_994348650619937
```

**What it returns:**
- Only 8 key fields per ad (vs 40+ in comprehensive)
- ad_id, ad_name, campaign_id, campaign_name, adset_id, adset_name
- spend, impressions, clicks, ctr, cpc, cpm, conversions, cpa
- Account-level summary with totals

**Benefit:** 80% smaller response, fits easily in context

**Best For:** Quick checks, weekly reviews, high-level overview

---

## ✅ SOLUTION 3: Reduce Limit Parameter

Instead of fetching 100 ads:
```
Get summary report for act_994348650619937 (limit: 100)
```

Use:
```
Get summary report for act_994348650619937 (limit: 25)
```

**Benefit:** Fetch fewer ads at a time, analyze in batches

**Best For:** When you want to analyze smaller segments at a time

---

## ✅ SOLUTION 4: Focus on Specific Campaigns

Use campaign-level insights instead of account-wide:
```
Get campaign insights for campaign_6770765233220 for last 30 days
```

**Benefit:** Only fetch data for campaigns you care about

**Best For:** Campaign-specific optimization

---

## ✅ SOLUTION 5: Use Shorter Date Ranges

Instead of:
```
last_30d
```

Use:
```
last_7d
```

**Benefit:** Less historical data = smaller response

**Best For:** Recent performance analysis, weekly check-ins

---

## ✅ SOLUTION 6: Sequential Analysis

**Strategy:** Analyze data in phases, summarize between phases

**Example workflow:**
```
Phase 1: Get summary report → Save key metrics
Phase 2: Identify top 5 performers → Deep dive on each
Phase 3: Identify bottom 5 performers → Analyze why
Phase 4: Create action plan based on phases 1-3
```

**Benefit:** Claude can "forget" detailed data after summarizing, freeing context for next phase

---

## 📊 COMPARISON TABLE

| Approach | Data Returned | Context Used | Time | Best For |
|----------|---------------|--------------|------|----------|
| Summary Report (100 ads) | ~8 fields × 100 ads | 🟡 Medium | 2 mins | Standard analysis |
| Summary Report (50 ads) | ~8 fields × 50 ads | 🟢 Low | 2 mins | Quick checks |
| Summary Report (25 ads) | ~8 fields × 25 ads | 🟢 Very Low | 1 min | Batch analysis |
| Modular Audit | Varies by module | 🟡 Medium | 5-60 mins | Thorough analysis |
| Campaign Insights | Campaign-level only | 🟢 Low | 1 min | Campaign optimization |

---

## 🎯 RECOMMENDED WORKFLOWS

### Daily Quick Check (5 mins)
```
1. Get summary report for last 7 days
2. Identify any CPA spikes
3. Check top/bottom 3 performers
```
**Tool:** `get_summary_report()`

### Weekly Review (30 mins)
```
1. Module 1: Account Snapshot
2. Module 2: Top Performers
3. Module 3: Underperformers  
4. Module 6: Weekly Trends
5. Quick wins summary
```
**File:** `MODULAR_AUDIT_PROMPT.md`

### Monthly Deep Dive (2 hours)
```
Run all 10 modules from MODULAR_AUDIT_PROMPT.md sequentially
Save output after each module
Combine insights at the end
```
**File:** `MODULAR_AUDIT_PROMPT.md`

### Campaign Optimization (20 mins)
```
1. Get summary report to identify underperformers
2. Get campaign insights for specific underperforming campaigns
3. Analyze ad sets and targeting
4. Create action plan
```
**Tools:** `get_summary_report()` → `get_campaign_insights(campaign_id=X)`

---

## 🚀 QUICK COMMANDS

**Lightweight (recommended):**
```
Get summary report for act_994348650619937 for last 30 days
```

**Even lighter (fewer ads):**
```
Get summary report for act_994348650619937 for last 30 days (limit: 25)
```

**Campaign-specific:**
```
Get campaign insights for campaign_6770765233220 for last 30 days
```

**Module 1 only:**
```
[Copy Module 1 from MODULAR_AUDIT_PROMPT.md]
```

---

## 💡 PRO TIPS

1. **Start with summary, drill down as needed**
   - Use `get_summary_report()` first to identify what needs deeper analysis
   - Then use `get_campaign_insights()` on specific campaigns for details

2. **Ask Claude to summarize frequently**
   - After each module: "Summarize key findings in 3-5 bullets"
   - This frees up context for next module

3. **Save outputs externally**
   - Copy important data to a doc
   - Don't rely on keeping everything in Claude's context

4. **Use specific date ranges**
   - `last_7d` for recent trends
   - `last_30d` for monthly reviews
   - Custom `time_range` for specific periods

5. **Batch similar analyses**
   - Analyze all top performers together
   - Then analyze all underperformers together
   - Don't mix and match

---

## 🔧 WHEN STILL HITTING LIMITS

If you still hit context limits:

1. **Reduce limit further:** Try `limit: 10` or `limit: 5`
2. **Use summary tool exclusively:** Stick with `get_summary_report()` only
3. **Analyze one campaign at a time:** Complete analysis before moving to next
4. **Break modules into sub-modules:** Split "Top Performers" into separate requests
5. **Restart conversation:** Start fresh with specific question

---

**Remember:** The modular approach is your best friend for comprehensive analysis without hitting limits! 🎯
