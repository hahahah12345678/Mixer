import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Upload, Music, Wand2, Download, Trash2, Play } from 'lucide-react';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [mixPrompt, setMixPrompt] = useState('');
  const [tempo, setTempo] = useState(100);
  const [mixStyle, setMixStyle] = useState('balanced');
  const [aiModel, setAiModel] = useState('gemini');
  const [isUploading, setIsUploading] = useState(false);
  const [isMixing, setIsMixing] = useState(false);
  const [mixedAudio, setMixedAudio] = useState(null);
  const [notification, setNotification] = useState('');

  const showNotification = (message) => {
    setNotification(message);
    setTimeout(() => setNotification(''), 3000);
  };

  const onDrop = useCallback(async (acceptedFiles) => {
    setIsUploading(true);
    const formData = new FormData();
    
    acceptedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadedFiles([...uploadedFiles, ...response.data.files]);
      showNotification(`${acceptedFiles.length} file(s) uploaded successfully!`);
    } catch (error) {
      console.error('Upload error:', error);
      showNotification('Error uploading files. Please try again.');
    } finally {
      setIsUploading(false);
    }
  }, [uploadedFiles]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.m4a']
    }
  });

  const handleMix = async () => {
    if (uploadedFiles.length === 0) {
      showNotification('Please upload at least one audio file');
      return;
    }

    if (!mixPrompt.trim()) {
      showNotification('Please enter a mixing prompt');
      return;
    }

    setIsMixing(true);

    try {
      const fileIds = uploadedFiles.map(f => f.id).join(',');
      const formData = new FormData();
      formData.append('file_ids', fileIds);
      formData.append('prompt', mixPrompt);
      formData.append('tempo', tempo);
      formData.append('style', mixStyle);
      formData.append('ai_model', aiModel);

      const response = await axios.post(`${API_URL}/mix`, formData);
      setMixedAudio(response.data);
      showNotification('Mix created successfully!');
    } catch (error) {
      console.error('Mix error:', error);
      showNotification('Error creating mix. Please try again.');
    } finally {
      setIsMixing(false);
    }
  };

  const handleDownload = () => {
    if (mixedAudio) {
      window.open(`${API_URL}/download/${mixedAudio.output_id}`, '_blank');
    }
  };

  const handlePlayMixed = () => {
    if (mixedAudio) {
      const audio = new Audio(`${API_URL}/download/${mixedAudio.output_id}`);
      audio.play();
    }
  };

  const removeFile = async (fileId) => {
    try {
      await axios.delete(`${API_URL}/files/${fileId}`);
      setUploadedFiles(uploadedFiles.filter(f => f.id !== fileId));
      showNotification('File removed');
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  return (
    <div className="App">
      {notification && (
        <div className="notification">
          {notification}
        </div>
      )}

      <div className="container">
        <header className="header">
          <Music className="logo-icon" size={48} />
          <h1>AI Music Mixer</h1>
          <p>Upload your MP3 files and let AI create amazing remixes</p>
        </header>

        <div className="upload-section">
          <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
            <input {...getInputProps()} />
            <Upload size={48} />
            {isDragActive ? (
              <p>Drop your audio files here...</p>
            ) : (
              <>
                <p>Drag & drop audio files here, or click to browse</p>
                <small>Supports MP3, WAV, and M4A files</small>
              </>
            )}
          </div>

          {isUploading && <div className="loading">Uploading files...</div>}

          {uploadedFiles.length > 0 && (
            <div className="file-list">
              <h3>Uploaded Files ({uploadedFiles.length})</h3>
              {uploadedFiles.map(file => (
                <div key={file.id} className="file-item">
                  <Music size={20} />
                  <span>{file.original_name}</span>
                  <button 
                    onClick={() => removeFile(file.id)}
                    className="btn-icon"
                    title="Remove file"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="mixer-section">
          <h2><Wand2 size={24} /> Mix Your Music</h2>
          
          <div className="form-group">
            <label>Mixing Prompt</label>
            <textarea
              value={mixPrompt}
              onChange={(e) => setMixPrompt(e.target.value)}
              placeholder="Describe how you want your mix to sound... (e.g., 'Create an energetic remix with heavy bass and smooth transitions')"
              rows="4"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Tempo: {tempo}%</label>
              <input
                type="range"
                min="50"
                max="200"
                value={tempo}
                onChange={(e) => setTempo(parseInt(e.target.value))}
                className="slider"
              />
            </div>

            <div className="form-group">
              <label>Mix Style</label>
              <select 
                value={mixStyle} 
                onChange={(e) => setMixStyle(e.target.value)}
                className="select"
              >
                <option value="balanced">Balanced Mix</option>
                <option value="layered">Layered (Overlay)</option>
                <option value="sequence">Sequential</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>🤖 AI Model</label>
            <select 
              value={aiModel} 
              onChange={(e) => setAiModel(e.target.value)}
              className="select ai-select"
            >
              <option value="gemini">✨ Google Gemini Flash (Recommended)</option>
              <option value="gpt4">⚡ GPT-4 Mini</option>
            </select>
            <small className="model-desc">
              {aiModel === 'gemini' 
                ? 'Fast and creative mixing suggestions' 
                : 'Precise and detailed audio analysis'}
            </small>
          </div>

          <button 
            onClick={handleMix}
            disabled={isMixing || uploadedFiles.length === 0}
            className="btn-primary"
          >
            {isMixing ? 'Creating Mix...' : 'Create Mix'}
          </button>

          {mixedAudio && (
            <div className="result-section">
              <h3>✨ Your Mix is Ready!</h3>
              <p className="prompt-display">Prompt: "{mixedAudio.prompt}"</p>
              <p className="model-used">AI Model: {mixedAudio.ai_model === 'gemini' ? '✨ Gemini Flash' : '⚡ GPT-4 Mini'}</p>
              <div className="result-actions">
                <button onClick={handlePlayMixed} className="btn-play">
                  <Play size={20} />
                  Play
                </button>
                <button onClick={handleDownload} className="btn-download">
                  <Download size={20} />
                  Download Mix
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
