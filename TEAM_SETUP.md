# 👥 Team Setup Guide - Facebook Ads MCP Server

Quick and easy setup for team members. Takes **5 minutes**.

---

## 🚀 One-Command Install (Recommended)

Open Terminal and run:

```bash
curl -sSL https://raw.githubusercontent.com/David-mo/fb-ads-mcp-server/main/install.sh | bash
```

This will:
- ✅ Check Python version (3.10+ required)
- ✅ Clone the repository
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Show you exactly what to do next

---

## 📋 Manual Install (Alternative)

If you prefer manual setup:

### Step 1: Install Python 3.12

**macOS:**
```bash
brew install python@3.12
```

**Windows:**
Download from https://www.python.org/downloads/

### Step 2: Clone Repository

```bash
git clone https://github.com/David-mo/fb-ads-mcp-server.git
cd fb-ads-mcp-server
```

### Step 3: Setup Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Get Your Facebook Access Token

1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your **Meta Business App**
3. Click **"Get User Access Token"**
4. Select permissions:
   - ✅ `ads_read`
   - ✅ `ads_management`
   - ✅ `business_management`
5. Click **"Generate Access Token"**
6. **Copy the token** (starts with `EAA...`)

**💡 Pro Tip:** Generate a **long-lived token** (60 days) or use a **System User token** (doesn't expire)

---

## ⚙️ Configure Claude Desktop

### macOS

1. Open the config file:
   ```bash
   open ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. Add this configuration (replace paths and token):
   ```json
   {
     "mcpServers": {
       "fb-ads-mcp-server": {
         "command": "/Users/YOUR_USERNAME/fb-ads-mcp-server/venv/bin/python",
         "args": [
           "/Users/YOUR_USERNAME/fb-ads-mcp-server/server.py",
           "--fb-token",
           "YOUR_FACEBOOK_TOKEN_HERE"
         ]
       }
     }
   }
   ```

### Windows

1. Open the config file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add this configuration:
   ```json
   {
     "mcpServers": {
       "fb-ads-mcp-server": {
         "command": "C:\\Users\\YOUR_USERNAME\\fb-ads-mcp-server\\venv\\Scripts\\python.exe",
         "args": [
           "C:\\Users\\YOUR_USERNAME\\fb-ads-mcp-server\\server.py",
           "--fb-token",
           "YOUR_FACEBOOK_TOKEN_HERE"
         ]
       }
     }
   }
   ```

**⚠️ Important:**
- Replace `YOUR_USERNAME` with your actual username
- Replace `YOUR_FACEBOOK_TOKEN_HERE` with your token
- Use **double backslashes** (`\\`) on Windows

---

## 🔄 Restart Claude Desktop

1. **Quit** Claude Desktop completely (⌘Q on Mac, Alt+F4 on Windows)
2. **Reopen** Claude Desktop
3. Wait 5-10 seconds for MCP servers to initialize

---

## ✅ Test the Setup

In Claude Desktop, ask:

```
List my Facebook ad accounts
```

If you see your ad accounts, **it works!** 🎉

---

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'mcp'"

**Fix:** You need Python 3.10 or higher
```bash
# Check version
python3 --version

# If < 3.10, install Python 3.12
brew install python@3.12  # macOS
```

Then recreate the virtual environment:
```bash
cd fb-ads-mcp-server
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "ValueError: Facebook access token not provided"

**Fix:** Check your Claude Desktop config file:
- Make sure `--fb-token` is followed by your actual token
- Token should be a long string starting with `EAA...`
- No spaces or quotes around the token value in the JSON

### "MCP server not detected in Claude Desktop"

**Fix:**
1. Check Claude Desktop logs:
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```
2. Look for error messages
3. Verify Python path is correct in config
4. Make sure you restarted Claude Desktop

### "Connection refused" or "Server failed to start"

**Fix:**
1. Check if Python virtual environment exists:
   ```bash
   ls -la ~/fb-ads-mcp-server/venv/bin/python
   ```
2. If not found, recreate it (see above)
3. Verify all paths in Claude config are absolute paths

---

## 🔄 Updating the Server

When there are updates to the MCP server:

```bash
cd ~/fb-ads-mcp-server
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

Then restart Claude Desktop.

---

## 🔐 Security Best Practices

### Keep Your Token Secure

- ✅ **DO:** Store token only in your local Claude config file
- ✅ **DO:** Use a System User token for production
- ✅ **DO:** Rotate tokens every 60 days
- ❌ **DON'T:** Share tokens in Slack/email
- ❌ **DON'T:** Commit tokens to GitHub
- ❌ **DON'T:** Use personal tokens for shared services

### Token Permissions

Only grant what's needed:
- **Read-only tasks:** Just `ads_read`
- **Campaign management:** Add `ads_management`
- **Account-level access:** Add `business_management`

---

## 📚 Available Tools

Once set up, you can ask Claude to:

**Account Management:**
- "List my Facebook ad accounts"
- "Get details for account act_123456789"

**Campaign Analysis:**
- "Show me all campaigns for account act_123456789"
- "Get campaign insights for last 30 days"

**Performance Reports:**
- "Get comprehensive ad report for last 7 days"
- "Get summary report for account act_123456789"

**Ad Set & Ad Details:**
- "Show me ad sets for campaign 6770765233220"
- "Get all ads in ad set 6989604267220"

See `README.md` for complete list of tools and examples.

---

## 🆘 Need Help?

- **Documentation:** Check `README.md` in the repo
- **GitHub Issues:** https://github.com/David-mo/fb-ads-mcp-server/issues
- **Team Chat:** Ask in your team Slack/Discord

---

## 🎯 Quick Reference

**Install command:**
```bash
curl -sSL https://raw.githubusercontent.com/David-mo/fb-ads-mcp-server/main/install.sh | bash
```

**Config location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Test command:**
```
List my Facebook ad accounts
```

**Update command:**
```bash
cd ~/fb-ads-mcp-server && git pull && pip install -r requirements.txt --upgrade
```

---

**🎉 You're all set! Start analyzing your Meta Ads with AI! 🚀**

