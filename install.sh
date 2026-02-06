#!/bin/bash

echo "🎵 AI Music Mixer - Installation Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg is not installed. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y ffmpeg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ffmpeg
    else
        echo "Please install ffmpeg manually for audio processing."
        exit 1
    fi
fi

echo ""
echo "📦 Installing Backend Dependencies..."
cd backend
python3 -m pip install -r requirements.txt

echo ""
echo "📦 Installing Frontend Dependencies..."
cd ../frontend
npm install

echo ""
echo "✅ Installation Complete!"
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && python3 main.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Don't forget to configure your .env file in the backend directory!"
