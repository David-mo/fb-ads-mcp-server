# META ADS AUDIT GUIDE

This guide shows you how to use the Facebook Ads MCP Server to conduct comprehensive account audits.

---

## 📁 AVAILABLE AUDIT PROMPTS

### 1. **QUICK_AUDIT_PROMPT.md**
- **Use when:** You need a fast audit (30-45 minutes)
- **Best for:** Weekly check-ins, quick performance reviews
- **Outputs:** Executive summary with top 3 quick wins

### 2. **META_AUDIT_PROMPT.md**  
- **Use when:** You need a deep, comprehensive audit (2-4 hours)
- **Best for:** Monthly/quarterly reviews, new account takeovers, major optimizations
- **Outputs:** Full 14-step analysis with detailed action plan

---

## 🚀 HOW TO RUN AN AUDIT

### Step 1: Ensure MCP Server is Running

Check Claude Desktop MCP status - you should see `fb-ads-mcp-server` as "running"

### Step 2: Choose Your Audit Type

**For Quick Audit:**
```bash
cat /Users/davidmorneau/METAMCP/fb-ads-mcp-server/QUICK_AUDIT_PROMPT.md
```

**For Comprehensive Audit:**
```bash
cat /Users/davidmorneau/METAMCP/fb-ads-mcp-server/META_AUDIT_PROMPT.md
```

### Step 3: Customize the Prompt

Replace these placeholders:
- `[ACCOUNT_ID]` → Your account ID (e.g., `act_994348650619937`)
- `[START_DATE]` → Start date in YYYY-MM-DD format
- `[END_DATE]` → End date in YYYY-MM-DD format

### Step 4: Paste into Claude Desktop

Copy the entire prompt and paste it into Claude Desktop

### Step 5: Review & Export Results

Claude will use the MCP tools to:
- Fetch all account data
- Analyze performance
- Generate recommendations
- Create executive summary

Export the results as:
- **Markdown** for documentation
- **PDF** for client reports
- **Spreadsheet** for data analysis

---

## 🎯 WHAT EACH AUDIT COVERS

### Quick Audit (10 Steps):
1. ✅ Account access verification
2. ✅ Account health metrics
3. ✅ Campaign structure overview
4. ✅ Performance metrics (last 30 days)
5. ✅ Top/bottom performers
6. ✅ Creative analysis
7. ✅ Audience insights
8. ✅ Quick win recommendations
9. ✅ Budget reallocation opportunities
10. ✅ Executive summary

### Comprehensive Audit (14 Steps):
1. ✅ Account overview & health check
2. ✅ Campaign structure analysis
3. ✅ Performance metrics deep dive
4. ✅ Creative performance analysis
5. ✅ Audience & targeting analysis
6. ✅ Budget allocation & pacing
7. ✅ Conversion funnel analysis
8. ✅ Time-based performance trends
9. ✅ Ad set & placement analysis
10. ✅ Creative testing framework evaluation
11. ✅ Campaign naming & organization
12. ✅ Competitive benchmarking
13. ✅ Prioritized recommendations
14. ✅ Executive summary & action plan

---

## 💡 BEST PRACTICES

### Before Running Audit:
- [ ] Verify MCP server is connected
- [ ] Confirm date range for analysis
- [ ] Note any specific concerns/questions
- [ ] Have access to previous reports for comparison

### During Audit:
- [ ] Let Claude complete all steps before asking follow-ups
- [ ] Save intermediate results if audit is interrupted
- [ ] Note any data anomalies or surprising findings

### After Audit:
- [ ] Export results immediately
- [ ] Share with stakeholders
- [ ] Create action items in project management tool
- [ ] Schedule follow-up audit (30 days)

---

## 📊 SAMPLE QUESTIONS TO ASK

After the audit completes, you can ask Claude:

**Performance Deep Dives:**
- "Which campaigns have the highest frequency? Is there creative fatigue?"
- "Show me the conversion funnel for Campaign X"
- "Compare last 7 days vs previous 7 days performance"

**Creative Analysis:**
- "What are the common patterns in top-performing video ads?"
- "Which ad creatives have been running longest without refresh?"
- "Show me engagement rates by creative format"

**Budget & Optimization:**
- "If I had an extra $1000/day, where should I allocate it?"
- "Which campaigns should I pause immediately?"
- "Calculate the ROAS for each campaign"

**Targeting Insights:**
- "What targeting strategies work best for Campaign X?"
- "Show me audience overlap between top campaigns"
- "Which demographics convert best?"

---

## 🔧 TROUBLESHOOTING

### "No data returned"
- Check account ID format (must be `act_XXXXXX`)
- Verify date range is valid
- Ensure MCP server has valid access token

### "All metrics are null"
- Restart Claude Desktop to load latest code
- Check if ads had spend in the date range
- Verify the spend filter is working

### "Audit taking too long"
- Use Quick Audit for faster results
- Narrow date range (e.g., last 7 days instead of 30)
- Focus on specific campaigns instead of all

### "MCP server failed"
- Check logs: `~/Library/Logs/Claude/mcp-server-fb-ads-mcp-server.log`
- Verify Python 3.10+ is installed
- Confirm access token is valid

---

## 📅 RECOMMENDED AUDIT CADENCE

### Weekly:
- Quick Audit (30 mins)
- Focus: Performance trends, quick wins

### Monthly:
- Comprehensive Audit (2-3 hours)
- Focus: Strategic optimizations, testing results

### Quarterly:
- Full Audit + Competitive Analysis
- Focus: Account structure, long-term strategy

### Ad-Hoc:
- When spending >30% more than usual
- After major campaign launches
- When CPA increases >20%
- Before client/stakeholder meetings

---

## 🎓 LEARNING FROM AUDITS

Keep a log of:
1. **Audit date**
2. **Key findings**
3. **Recommendations made**
4. **Actions taken**
5. **Results (30 days later)**

This creates a performance history and shows optimization impact over time.

---

## 📧 AUDIT REPORT TEMPLATE

Use this structure when sharing results:

**Subject:** Meta Ads Account Audit - [Account Name] - [Date]

**To:** [Stakeholders]

**Summary:**
- Account health score: X/100
- Total spend analyzed: $X
- Key finding: [1-2 sentences]

**Recommended Actions:**
1. [Priority 1 - Expected impact]
2. [Priority 2 - Expected impact]  
3. [Priority 3 - Expected impact]

**Full Report:** [Attach/Link]

**Next Steps:**
- Implement recommendations by [Date]
- Review results on [Date]
- Next audit scheduled for [Date]

---

## 🚀 QUICK START

**First Time Running Audit:**

```bash
# 1. View the quick audit prompt
cat /Users/davidmorneau/METAMCP/fb-ads-mcp-server/QUICK_AUDIT_PROMPT.md

# 2. Replace act_994348650619937 with your account ID

# 3. Copy and paste into Claude Desktop

# 4. Wait for analysis to complete (5-15 minutes)

# 5. Review recommendations and take action!
```

---

**Happy Auditing! 🎯**

For questions or issues, check:
- GitHub: https://github.com/David-mo/fb-ads-mcp-server
- Server logs: `~/Library/Logs/Claude/mcp-server-fb-ads-mcp-server.log`
- README: `/Users/davidmorneau/METAMCP/fb-ads-mcp-server/README.md`
