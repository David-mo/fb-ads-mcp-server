#!/bin/bash
# Facebook Ads MCP Server - Easy Team Setup Script
# Usage: curl -sSL https://raw.githubusercontent.com/David-mo/fb-ads-mcp-server/main/install.sh | bash

set -e

echo "🚀 Installing Facebook Ads MCP Server..."
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

if [ "$MACHINE" = "UNKNOWN:${OS}" ]; then
    echo "❌ Unsupported operating system: ${OS}"
    exit 1
fi

echo "✅ Detected: $MACHINE"
echo ""

# Check Python version
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD=python3.10
elif command -v python3 &> /dev/null; then
    VERSION=$($python3 --version 2>&1 | awk '{print $2}')
    MAJOR=$(echo $VERSION | cut -d. -f1)
    MINOR=$(echo $VERSION | cut -d. -f2)
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
        PYTHON_CMD=python3
    else
        echo "❌ Python 3.10+ required. Found: $VERSION"
        echo "📥 Install Python 3.12:"
        if [ "$MACHINE" = "Mac" ]; then
            echo "   brew install python@3.12"
        else
            echo "   Visit: https://www.python.org/downloads/"
        fi
        exit 1
    fi
else
    echo "❌ Python 3.10+ not found"
    echo "📥 Install Python:"
    if [ "$MACHINE" = "Mac" ]; then
        echo "   brew install python@3.12"
    else
        echo "   Visit: https://www.python.org/downloads/"
    fi
    exit 1
fi

echo "✅ Found Python: $PYTHON_CMD"
echo ""

# Set installation directory
if [ -z "$INSTALL_DIR" ]; then
    INSTALL_DIR="$HOME/fb-ads-mcp-server"
fi

echo "📂 Installing to: $INSTALL_DIR"
echo ""

# Clone repository
if [ -d "$INSTALL_DIR" ]; then
    echo "📁 Directory exists, pulling latest changes..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/David-mo/fb-ads-mcp-server.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✅ Installation complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Get your Facebook Access Token:"
echo "   https://developers.facebook.com/tools/explorer/"
echo ""
echo "2️⃣  Configure Claude Desktop:"
echo ""
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "   Add this configuration:"
echo ""
echo '   {
     "mcpServers": {
       "fb-ads-mcp-server": {
         "command": "'$INSTALL_DIR'/venv/bin/python",
         "args": [
           "'$INSTALL_DIR'/server.py",
           "--fb-token",
           "YOUR_FACEBOOK_TOKEN_HERE"
         ]
       }
     }
   }'
echo ""
echo "3️⃣  Restart Claude Desktop"
echo ""
echo "4️⃣  Test by asking: \"List my Facebook ad accounts\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Documentation: $INSTALL_DIR/README.md"
echo "🆘 Issues: https://github.com/David-mo/fb-ads-mcp-server/issues"
echo ""
echo "🎉 Happy advertising! 🚀"
echo ""

