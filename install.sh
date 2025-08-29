#!/bin/bash

# VAPI AI Assistant Manager - Installation Script
# This script sets up the application environment and dependencies

echo "🤖 VAPI AI Assistant Manager - Installation Script"
echo "=================================================="

# Check if Python 3.11+ is available
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$PYTHON_VERSION >= 3.11" | bc -l) )); then
        PYTHON_CMD="python3"
    else
        echo "❌ Python 3.11 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Using Python: $PYTHON_CMD"

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✅ Using pip: $PIP_CMD"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# Check if .env file exists, if not create from example
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo ""
        echo "📝 Creating .env file from template..."
        cp .env.example .env
        echo "✅ .env file created. Please edit it with your API credentials."
        echo ""
        echo "⚠️  IMPORTANT: Edit the .env file and add your VAPI AI API key:"
        echo "   nano .env"
        echo "   or"
        echo "   code .env"
    fi
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   streamlit run app_improved.py"
echo ""
echo "📖 Then open your browser to: http://localhost:8501"
echo ""
echo "⚙️  Don't forget to:"
echo "   1. Get your API key from https://dashboard.vapi.ai"
echo "   2. Configure it in the Settings page or .env file"
echo "   3. Test the connection before creating assistants"
echo ""
echo "📚 For more information, see README.md and DEPLOYMENT.md"
echo ""
echo "Happy voice assistant building! 🤖✨"

