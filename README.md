# 🎵 AI Music Mixer

An AI-powered web application that allows you to upload MP3 files and create custom remixes using artificial intelligence. Mix multiple tracks, apply effects, and generate unique versions of your favorite songs!

## ✨ Features

- 🎧 **Multi-File Upload**: Upload multiple MP3, WAV, or M4A audio files
- 🤖 **AI-Powered Mixing**: Choose between GPT-4 Mini or Gemini Flash for intelligent mixing suggestions
- 🎚️ **Customizable Controls**: Adjust tempo, mixing style, and effects
- 📥 **Download & Play**: Listen to and download your custom mixes
- 🎨 **Beautiful UI**: Modern, responsive interface with drag-and-drop support
- ⚡ **Dual AI Models**: 
  - **Gemini Flash**: Fast, creative mixing suggestions (Recommended)
  - **GPT-4 Mini**: Precise, detailed audio analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- ffmpeg (for audio processing)

### Installation

1. **Clone the repository:**
```bash
cd /workspaces/Mixer
```

2. **Run the installation script:**
```bash
chmod +x install.sh
./install.sh
```

Or install manually:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

3. **Configure environment variables:**
```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys if needed
```

### Running the Application

**Option 1: Use the start script**
```bash
chmod +x start.sh
./start.sh
```

**Option 2: Start services manually**

Backend:
```bash
cd backend
python3 main.py
```

Frontend (in a new terminal):
```bash
cd frontend
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## 🎮 How to Use

1. **Upload Audio Files**: Drag and drop MP3, WAV, or M4A files into the upload area
2. **Select AI Model**: Choose between Gemini Flash (fast & creative) or GPT-4 Mini (precise)
3. **Describe Your Mix**: Enter a prompt describing how you want your mix to sound (e.g., "Create an energetic remix with heavy bass")
4. **Adjust Settings**: 
   - Set the tempo (50-200%)
   - Choose a mixing style (Balanced, Layered, or Sequential)
5. **Create Mix**: Click "Create Mix" to let AI generate your custom remix
6. **Play or Download**: Listen to your mix or download it to your device

## 🎛️ Mixing Styles

- **Balanced**: Mixes all tracks together with volume adjustments
- **Layered**: Overlays all tracks on top of each other
- **Sequential**: Plays tracks one after another

## 🧠 AI Prompt Examples

- "Create an energetic remix with heavy bass and smooth transitions"
- "Make it light and airy with soft vocals"
- "Add powerful bass and make it louder"
- "Smooth fade-in and fade-out effects"
- "Professional club mix with deep bass"
- "Relaxing ambient mix with gentle transitions"

## 🤖 AI Models

### Gemini Flash (Recommended)
- **Speed**: Very Fast
- **Style**: Creative and innovative mixing suggestions
- **Best For**: Quick remixes, experimental mixes, creative combinations

### GPT-4 Mini
- **Speed**: Fast
- **Style**: Precise and detailed audio analysis
- **Best For**: Professional mixes, detailed control, specific requirements

## 📁 Project Structure

```
Mixer/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── uploads/            # Uploaded audio files
│   └── outputs/            # Generated mixes
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styles
│   │   └── index.js        # Entry point
│   ├── public/
│   │   └── index.html      # HTML template
│   └── package.json        # Node dependencies
├── install.sh              # Installation script
├── start.sh               # Start script
└── README.md              # This file
```

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Pydub**: Audio processing library
- **Uvicorn**: ASGI server
- **Python Multipart**: File upload handling

### Frontend
- **React**: UI library
- **React Dropzone**: Drag-and-drop file uploads
- **Axios**: HTTP client
- **Lucide React**: Icon library

## 🔧 API Endpoints

- `GET /` - API status
- `POST /upload` - Upload audio files
- `POST /mix` - Create a mix
- `GET /download/{output_id}` - Download mixed audio
- `DELETE /files/{file_id}` - Delete uploaded file

## 🎯 Future Enhancements

- Integration with advanced AI music generation models
- Real-time audio preview
- More mixing effects and filters
- User accounts and saved mixes
- Collaborative mixing features
- Waveform visualization
- BPM detection and auto-sync

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 💡 Tips

- For best results, use high-quality audio files
- Experiment with different prompts and settings
- The AI effects are based on keyword detection in your prompt
- Try mixing 2-4 tracks for optimal results

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure ffmpeg is installed: `ffmpeg -version`
- Check Python version: `python3 --version` (needs 3.8+)

**Frontend won't start:**
- Check Node version: `node --version` (needs 14+)
- Try deleting `node_modules` and running `npm install` again

**Can't upload files:**
- Check that the backend is running on port 8000
- Verify file format is supported (MP3, WAV, M4A)

---

Made with ❤️ for music lovers and creators!