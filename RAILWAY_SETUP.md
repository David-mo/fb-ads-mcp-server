# 🚂 Railway Deployment Guide - Remote MCP Server

This guide shows you how to deploy the Facebook Ads MCP Server to Railway and connect your entire team to it.

---

## 🎯 What You'll Get

- **Hosted MCP server** accessible via URL (like Activepieces/Foreplay)
- **Team members connect** via Claude Desktop config
- **Single source of truth** - one server, one token, everyone connected
- **Auto-updates** when you push to GitHub

---

## 📋 Prerequisites

1. Railway account (sign up at https://railway.app)
2. This GitHub repo
3. Facebook Ads access token

---

## 🚀 STEP 1: Deploy to Railway

### 1.1 Push Latest Code to GitHub

```bash
cd /Users/davidmorneau/METAMCP/fb-ads-mcp-server
git add -A
git commit -m "Add SSE transport for Railway deployment"
git push origin main
```

### 1.2 Create Railway Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose `fb-ads-mcp-server` repository
5. Railway will auto-detect Python and use the `Procfile`

### 1.3 Configure Environment Variables

In Railway project settings, add:

```
FB_ACCESS_TOKEN=YOUR_FACEBOOK_ACCESS_TOKEN_HERE
```

**Important:** Use a long-lived token or System User token from Meta Business.

### 1.4 Generate Public Domain

1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Railway will give you a URL like: `https://fb-ads-mcp-server-production.up.railway.app`

**Save this URL - your team will need it!**

---

## 💻 STEP 2: Configure Claude Desktop (Team Members)

Each team member needs to update their Claude Desktop configuration to connect to your Railway server.

### 2.1 Open Claude Desktop Config

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

###2.2 Add MCP Server Configuration

Replace `YOUR_RAILWAY_URL` with your actual Railway domain:

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "url": "https://fb-ads-mcp-server-production.up.railway.app/sse"
    }
  }
}
```

**Note:** The `/sse` endpoint is required for Server-Sent Events transport.

### 2.3 Restart Claude Desktop

1. Quit Claude Desktop completely (⌘Q on Mac)
2. Reopen Claude Desktop
3. The MCP server should now be connected

---

## ✅ STEP 3: Test the Connection

Open Claude Desktop and ask:

```
List my Facebook ad accounts
```

If it works, you'll see your ad accounts! 🎉

---

## 🔄 Updating the Server

When you make changes:

```bash
git add -A
git commit -m "Your changes"
git push origin main
```

Railway will **automatically redeploy** and your entire team gets the update - no action needed!

---

## 👥 Team Onboarding

Send this to new team members:

```
📱 **Facebook Ads MCP Server - Setup**

1. Open Claude Desktop
2. Go to Settings → Developer → Edit Config
3. Add this configuration:

{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "url": "https://fb-ads-mcp-server-production.up.railway.app/sse"
    }
  }
}

4. Restart Claude Desktop
5. Test by asking: "List my Facebook ad accounts"

Need help? Contact [YOUR NAME]
```

---

## 🔐 Security Best Practices

### Use System User Token

For production team deployments, use a **Meta System User** token instead of personal tokens:

1. Go to **Meta Business Settings**
2. **Users** → **System Users**
3. Create a new System User
4. Generate a token with appropriate permissions
5. Use this token in Railway's `FB_ACCESS_TOKEN` environment variable

### Token Permissions

Your token needs these permissions:
- `ads_read`
- `ads_management` (if you want to create/modify campaigns)
- `business_management`

### Rotate Tokens

Set a reminder to rotate tokens every 60 days.

---

## 🛠️ Troubleshooting

### "Cannot connect to MCP server"

**Check Railway logs:**
1. Go to Railway dashboard
2. Click your project
3. View **Logs** tab
4. Look for errors

**Common issues:**
- Token not set or expired
- Railway service not running
- Wrong URL in Claude config

### "Invalid token" errors

- Token may have expired (Meta tokens expire after 60 days)
- Regenerate token in Meta Business Manager
- Update `FB_ACCESS_TOKEN` in Railway
- Railway will auto-redeploy

### Railway URL shows `.railway.internal`

That's the **internal** URL. You need the **public** domain:
1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Use the public URL (e.g., `fb-ads-mcp-server-production.up.railway.app`)

---

## 💰 Costs

- **Railway Free Tier:** $5/month credit (enough for small teams)
- **Railway Hobby:** $5/month after free credit
- **Railway Pro:** $20/month for higher usage

Most small teams (3-10 people) stay within free tier limits.

---

## 📊 Monitoring

Monitor your Railway deployment:

1. **Logs:** Check for errors or API issues
2. **Metrics:** View CPU/memory usage
3. **Deployments:** Track updates and rollbacks

---

## 🎯 Local vs. Remote

You can still run the server locally for development:

```bash
python server.py --fb-token YOUR_TOKEN
```

This uses **stdio** transport (local only).

For team deployment, Railway uses **SSE** transport (remote access).

---

## 🆘 Need Help?

- Check Railway logs first
- Verify token is valid and not expired
- Test with: "List my Facebook ad accounts"
- Open an issue on GitHub

---

**You're all set! Your team can now use Facebook Ads MCP Server from anywhere! 🚀**

