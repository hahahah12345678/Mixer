# 🚀 Quick Setup Guide - AI Music Mixer

## API Keys Configuration

Your API keys have been configured in `/workspaces/Mixer/backend/.env`

⚠️ **Important Note**: Both API keys are currently set to the same value. Please verify:
- **OPENAI_API_KEY**: Should be your OpenAI API key (starts with `sk-`)
- **GOOGLE_API_KEY**: Should be your Google Cloud API key (already looks correct)

## Getting Started

### Step 1: Install Dependencies

```bash
cd /workspaces/Mixer
./install.sh
```

This will:
- Install Python packages (FastAPI, Pydub, OpenAI, Google Generative AI)
- Install Node.js packages (React, Axios, React Dropzone)
- Install ffmpeg for audio processing

### Step 2: Start the Application

```bash
./start.sh
```

Or start services manually:

**Terminal 1 - Backend:**
```bash
cd backend
python3 main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Step 3: Access the App

Open your browser to: **http://localhost:3000**

## 🎯 Using AI Models

### Gemini Flash (Default - Recommended)
- ✅ Fast response time
- ✅ Creative mixing suggestions
- ✅ Great for experimental mixes
- API Key: Already configured

### GPT-4 Mini
- ✅ Detailed audio analysis
- ✅ Precise recommendations
- ✅ Professional mixing advice
- API Key: Needs valid OpenAI key

## 🎵 Example Workflow

1. **Upload Files**: Drag 2-3 MP3 files
2. **Select Model**: Choose "Gemini Flash" or "GPT-4 Mini"
3. **Enter Prompt**: "Create an energetic dance remix with heavy bass"
4. **Adjust Settings**: 
   - Tempo: 120%
   - Style: Layered
5. **Create Mix**: Click the button
6. **Download**: Save your custom mix!

## 🔧 Troubleshooting

### API Key Issues

If you get API errors:

1. Check `/workspaces/Mixer/backend/.env` file
2. For OpenAI: Get key from https://platform.openai.com/api-keys
3. For Google: Get key from https://makersuite.google.com/app/apikey

### Model Selection

- **Gemini not working?** Check GOOGLE_API_KEY in .env
- **GPT-4 not working?** Check OPENAI_API_KEY in .env (should start with `sk-`)

Both models will fallback to rule-based mixing if API calls fail.

## 📝 API Key Format

**OpenAI Key Format:**
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Google API Key Format:**
```
AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Happy mixing! 🎶
