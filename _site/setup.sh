#!/bin/bash
# Setup script for Jekyll Post Wizard

set -e  # Exit on any error

echo "🧙 Setting up Jekyll Post Wizard..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3.6+ and try again"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Using Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Copy style template if style.txt doesn't exist
if [ ! -f "style.txt" ]; then
    echo "📝 Creating style.txt from template..."
    cp style_template.txt style.txt
    echo "✏️  Please customize style.txt with your writing preferences!"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file from template..."
    cp .env.template .env
    echo "🚨 Please add your ANTHROPIC_API_KEY to the .env file!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Anthropic API key to .env"
echo "2. Customize style.txt with your writing preferences"
echo "3. Generate your first post:"
echo "   ./generate.py 'Your blog post topic'"
echo ""
echo "To activate the environment later:"
echo "   source venv/bin/activate"