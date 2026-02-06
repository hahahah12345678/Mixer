from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
from typing import List
import uuid
from pydub import AudioSegment
import openai
from openai import OpenAI
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Music Mixer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure AI models
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None

# Create directories for uploads and outputs
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "AI Music Mixer API", "status": "running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple MP3 files"""
    uploaded_files = []
    
    for file in files:
        if not file.filename.endswith(('.mp3', '.wav', '.m4a')):
            raise HTTPException(status_code=400, detail=f"File {file.filename} must be an audio file (.mp3, .wav, .m4a)")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1]
        filename = f"{file_id}.{file_extension}"
        file_path = UPLOAD_DIR / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append({
            "id": file_id,
            "original_name": file.filename,
            "filename": filename,
            "path": str(file_path)
        })
    
    return {"files": uploaded_files, "message": "Files uploaded successfully"}

@app.post("/mix")
async def mix_audio(
    file_ids: str = Form(...),
    prompt: str = Form(...),
    tempo: int = Form(100),
    style: str = Form("balanced"),
    ai_model: str = Form("gemini")
):
    """Mix uploaded audio files based on AI prompt and parameters"""
    try:
        file_id_list = file_ids.split(',')
        
        # Load audio files
        audio_segments = []
        for file_id in file_id_list:
            # Find the file with this ID
            matching_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
            if not matching_files:
                raise HTTPException(status_code=404, detail=f"File {file_id} not found")
            
            file_path = matching_files[0]
            audio = AudioSegment.from_file(str(file_path))
            audio_segments.append(audio)
        
        # Apply basic mixing based on style
        if style == "layered":
            # Overlay all tracks
            mixed = audio_segments[0]
            for audio in audio_segments[1:]:
                mixed = mixed.overlay(audio)
        elif style == "sequence":
            # Concatenate tracks
            mixed = sum(audio_segments)
        else:  # balanced
            # Mix with volume adjustment
            mixed = audio_segments[0]
            for audio in audio_segments[1:]:
                mixed = mixed.overlay(audio - 3)  # Reduce volume slightly
        
        # Apply tempo adjustment
        if tempo != 100:
            speed_factor = tempo / 100
            mixed = mixed.speedup(playback_speed=speed_factor)
        
        # Apply AI-based effects based on prompt and model
        mixed = await apply_ai_effects(mixed, prompt, ai_model)
        
        # Export mixed audio
        output_id = str(uuid.uuid4())
        output_filename = f"{output_id}.mp3"
        output_path = OUTPUT_DIR / output_filename
        
        mixed.export(str(output_path), format="mp3", bitrate="192k")
        
        return {
            "output_id": output_id,
            "filename": output_filename,
            "message": "Audio mixed successfully",
            "prompt": prompt,
            "ai_model": ai_model
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def apply_ai_effects(audio: AudioSegment, prompt: str, ai_model: str) -> AudioSegment:
    """Apply effects based on AI analysis of the prompt"""
    
    # Get AI recommendations for audio processing
    ai_suggestions = await get_ai_mixing_suggestions(prompt, ai_model)
    
    prompt_lower = prompt.lower()
    
    # Apply AI-suggested effects
    if ai_suggestions:
        if 'bass' in ai_suggestions.lower():
            audio = audio.low_pass_filter(200).overlay(audio)
        if 'treble' in ai_suggestions.lower() or 'high' in ai_suggestions.lower():
            audio = audio.high_pass_filter(300)
        if 'fade' in ai_suggestions.lower():
            audio = audio.fade_in(2000).fade_out(2000)
    
    # Bass boost for energetic requests
    if any(word in prompt_lower for word in ['energetic', 'bass', 'heavy', 'powerful']):
        audio = audio.low_pass_filter(200).overlay(audio)
    
    # High pass for light/airy requests
    if any(word in prompt_lower for word in ['light', 'airy', 'soft', 'gentle']):
        audio = audio.high_pass_filter(300)
    
    # Fade effects for smooth requests
    if any(word in prompt_lower for word in ['smooth', 'fade', 'transition']):
        audio = audio.fade_in(2000).fade_out(2000)
    
    # Volume adjustments
    if 'loud' in prompt_lower or 'louder' in prompt_lower:
        audio = audio + 5
    elif 'quiet' in prompt_lower or 'softer' in prompt_lower:
        audio = audio - 5
    
    return audio

async def get_ai_mixing_suggestions(prompt: str, ai_model: str) -> str:
    """Get AI mixing suggestions from the selected model"""
    system_prompt = """You are an expert music producer and audio engineer. 
    Analyze the user's mixing request and suggest specific audio effects to apply.
    Be concise and mention specific effects like: bass boost, treble enhancement, 
    fade in/out, volume adjustment, reverb, compression, etc.
    Keep your response under 100 words."""
    
    try:
        if ai_model == "gpt4" and openai_client:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Mixing request: {prompt}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif ai_model == "gemini" and gemini_model:
            full_prompt = f"{system_prompt}\n\nMixing request: {prompt}"
            response = gemini_model.generate_content(full_prompt)
            return response.text
        
        else:
            return "Apply standard mixing techniques based on the prompt."
    
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return "Apply standard mixing techniques based on the prompt."

@app.get("/download/{output_id}")
async def download_mixed_audio(output_id: str):
    """Download the mixed audio file"""
    output_path = OUTPUT_DIR / f"{output_id}.mp3"
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(output_path),
        media_type="audio/mpeg",
        filename=f"mixed_{output_id}.mp3"
    )

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    matching_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    
    if not matching_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    matching_files[0].unlink()
    return {"message": "File deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
