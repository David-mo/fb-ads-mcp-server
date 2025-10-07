# TEAM DEPLOYMENT GUIDE - Facebook Ads MCP Server

This guide covers different options for deploying the MCP server for team access.

---

## 🎯 DEPLOYMENT OPTIONS

### Option 1: Cloud-Hosted MCP Server (Centralized)

Host a single MCP server instance that the entire team connects to.

#### A. Railway.app (Easiest - Recommended)

**Setup Steps:**

1. **Fork the GitHub repo** to your organization
2. **Go to Railway.app** and sign in with GitHub
3. **Create New Project** → Deploy from GitHub repo
4. **Add Environment Variables:**
   ```
   FB_ACCESS_TOKEN=your_token_here
   PORT=8000
   ```
5. **Deploy** - Railway auto-detects Python and runs the server
6. **Get URL** - Railway provides: `https://your-app.railway.app`

**Team Configuration:**

Each team member updates their `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fb-ads-mcp-server": {
      "command": "curl",
      "args": [
        "https://your-app.railway.app/mcp"
      ]
    }
  }
}
```

**Cost:** 
- Free tier: $5/month credit (enough for small teams)
- Pro: $20/month for higher usage

---

#### B. Render.com (Simple Alternative)

**Setup Steps:**

1. **Go to Render.com** and create account
2. **New Web Service** → Connect GitHub repo
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py --fb-token $FB_ACCESS_TOKEN`
4. **Add Environment Variable:**
   ```
   FB_ACCESS_TOKEN=your_token_here
   ```
5. **Deploy** - Get URL like `https://fb-ads-mcp.onrender.com`

**Cost:**
- Free tier available (spins down after inactivity)
- Paid: $7/month for always-on

---

#### C. AWS EC2 (Full Control)

**For larger teams or custom requirements**

**Setup Steps:**

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier) or t2.small
   - Open port 8000 in security group

2. **SSH into instance and install:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python 3.12
   sudo apt install python3.12 python3.12-venv python3-pip -y
   
   # Clone repo
   git clone https://github.com/David-mo/fb-ads-mcp-server.git
   cd fb-ads-mcp-server
   
   # Setup virtual environment
   python3.12 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set token as environment variable
   export FB_ACCESS_TOKEN="your_token_here"
   
   # Run server (use systemd for production)
   python server.py --fb-token $FB_ACCESS_TOKEN
   ```

3. **Create systemd service** (for auto-restart):
   ```bash
   sudo nano /etc/systemd/system/fb-ads-mcp.service
   ```
   
   ```ini
   [Unit]
   Description=Facebook Ads MCP Server
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/fb-ads-mcp-server
   Environment="FB_ACCESS_TOKEN=your_token_here"
   ExecStart=/home/ubuntu/fb-ads-mcp-server/venv/bin/python server.py --fb-token $FB_ACCESS_TOKEN
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   sudo systemctl enable fb-ads-mcp
   sudo systemctl start fb-ads-mcp
   ```

**Cost:**
- t2.micro: Free tier (1 year) then ~$8/month
- t2.small: ~$17/month

---

### Option 2: Local Installation for Each Team Member

**Best for:** Security-conscious teams, different access levels per person

**Distribution Method:**

1. **Create setup script** for your team:

```bash
#!/bin/bash
# team-setup.sh

echo "Setting up Facebook Ads MCP Server..."

# Clone repo
git clone https://github.com/David-mo/fb-ads-mcp-server.git
cd fb-ads-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your Facebook access token from: https://developers.facebook.com/tools/explorer/"
echo "2. Update Claude Desktop config with your token"
echo "3. Restart Claude Desktop"
echo ""
echo "Config file location:"
echo "macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
```

2. **Share documentation:**
   - README.md from the repo
   - Internal wiki/docs with your team's specific setup
   - Slack/Teams channel for support

3. **Token management:**
   - Each person gets their own token from Meta Business
   - Or use a shared "service account" token (less secure)

**Pros:**
- Maximum security
- No hosting costs
- Works offline

**Cons:**
- Setup required for each person
- Harder to update everyone
- Inconsistent versions possible

---

### Option 3: Docker Container (Portable)

**Best for:** Teams comfortable with Docker

**Create Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "server.py", "--fb-token", "$FB_ACCESS_TOKEN"]
```

**Deploy anywhere:**
- **Docker Hub** → Pull and run on any machine
- **AWS ECS/Fargate** → Serverless containers
- **Google Cloud Run** → Auto-scaling
- **Azure Container Instances** → Simple deployment

**Team usage:**
```bash
docker run -p 8000:8000 -e FB_ACCESS_TOKEN=your_token yourorg/fb-ads-mcp-server
```

---

## 🔐 SECURITY CONSIDERATIONS

### Token Management

**❌ DON'T:**
- Commit tokens to GitHub
- Share tokens in Slack/email
- Use personal tokens for team deployments

**✅ DO:**
- Use environment variables
- Create a dedicated service account token
- Rotate tokens regularly (every 60 days)
- Use Meta's System User tokens for production

### Access Control

**For cloud deployments:**

1. **Add authentication** to the MCP server:
   ```python
   # Add to server.py
   import os
   from functools import wraps
   
   API_KEY = os.environ.get('API_KEY')
   
   def require_api_key(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           key = request.headers.get('X-API-Key')
           if key != API_KEY:
               return {'error': 'Unauthorized'}, 401
           return f(*args, **kwargs)
       return decorated
   ```

2. **Use VPN** for internal-only access

3. **Whitelist IP addresses** in cloud provider settings

---

## 📊 COMPARISON TABLE

| Method | Setup Difficulty | Cost/Month | Security | Best For |
|--------|-----------------|------------|----------|----------|
| Railway.app | ⭐ Easy | $5-20 | Medium | Small teams (3-10) |
| Render.com | ⭐ Easy | $0-7 | Medium | Startups, small teams |
| AWS EC2 | ⭐⭐⭐ Hard | $8-50 | High | Large teams (10+) |
| Local Install | ⭐⭐ Medium | $0 | Highest | Security-focused |
| Docker | ⭐⭐ Medium | Varies | Medium-High | DevOps teams |

---

## 💡 RECOMMENDED APPROACH BY TEAM SIZE

### 1-3 People
→ **Local Installation** (Option 2)
- Everyone runs it on their own machine
- Share the GitHub repo + setup instructions
- Each person uses their own token

### 4-10 People
→ **Railway.app** (Option 1A)
- Easy to set up and maintain
- Affordable
- Good for getting started quickly
- Upgrade to AWS later if needed

### 10+ People or Enterprise
→ **AWS EC2 + VPN** (Option 1C)
- Full control
- Better security
- Dedicated resources
- Professional deployment

---

## 🚀 QUICK START: Railway Deployment

**5-Minute Team Setup:**

1. **Fork repo** to your GitHub org
2. **Go to Railway.app** → New Project → Deploy from GitHub
3. **Add environment variable:** `FB_ACCESS_TOKEN=your_token`
4. **Copy the Railway URL** (e.g., `https://fb-ads-mcp-production.up.railway.app`)
5. **Share with team:** Everyone updates their Claude Desktop config to point to Railway URL
6. **Done!** Team can now use the MCP server

---

## 📝 TEAM ONBOARDING TEMPLATE

**Send this to new team members:**

```
Welcome! Here's how to access our Facebook Ads MCP Server:

1. Open Claude Desktop
2. Go to Settings → Developer → MCP Servers
3. Add this configuration:

{
  "fb-ads-mcp-server": {
    "url": "https://our-company-mcp.railway.app"
  }
}

4. Restart Claude Desktop
5. Test it by asking: "List my Facebook ad accounts"

Need help? Check our wiki or ask in #marketing-tech Slack channel.
```

---

## 🔄 UPDATE WORKFLOW

**For cloud deployments:**
1. Push changes to GitHub
2. Cloud platform auto-deploys (Railway/Render)
3. Team automatically gets updates (no action needed)

**For local installations:**
1. Push changes to GitHub
2. Team members run: `git pull && pip install -r requirements.txt`
3. Restart Claude Desktop

---

## 🆘 TROUBLESHOOTING

**"Connection refused"**
- Check if server is running: `systemctl status fb-ads-mcp`
- Check firewall/security group allows port 8000

**"Invalid token"**
- Token may have expired (Meta tokens expire after 60 days)
- Regenerate token in Meta Business Manager
- Update environment variable

**"Slow response times"**
- Upgrade server instance (more CPU/RAM)
- Add caching layer (Redis)
- Optimize API calls (use summary report instead of comprehensive)

---

**Questions? Open an issue on GitHub or contact your team admin.**

