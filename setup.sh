#!/bin/bash

# Setup script for Databricks Table Viewer App

set -e

echo "🚀 Setting up Databricks Table Viewer App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Databricks credentials."
else
    echo "✅ .env file already exists"
fi

# Check if Databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo ""
    echo "⚠️  Databricks CLI not found. To install, run:"
    echo "   curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh"
    echo ""
else
    echo "✅ Databricks CLI found: $(databricks --version)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env with your Databricks credentials"
echo "   2. Activate the virtual environment: source venv/bin/activate"
echo "   3. Run the app locally: streamlit run app.py"
echo "   4. Or deploy to Databricks: databricks bundle deploy -t dev"
echo ""

