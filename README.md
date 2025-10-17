# 🎙️ Audio Transcription Web App using OpenAI Whisper

A **full-stack AI-powered web application** that transcribes large audio files into text using **OpenAI Whisper**.  
Built with **React (frontend)** and **Flask (backend)** — designed to be **fast, secure, and capable of handling long audio files (up to ~30 minutes)**.

---

## 🚀 Features

✅ Transcribe long audio files (up to 30 minutes)  
✅ Supports multiple audio formats (`.mp3`, `.wav`, `.m4a`, `.ogg`)  
✅ Clean and modern user interface  
✅ Fast processing using OpenAI’s Whisper model  
✅ Secure backend with API key protection  
✅ Responsive design for all screen sizes  
✅ Automatic paragraph formatting for transcripts  
✅ Real-time progress updates  

---

## 🧠 Tech Stack

| Layer          | Technology |
|----------------|----------------------|
| **Frontend**   | React, HTML5, CSS3, JavaScript |
| **Backend**    | Python, Flask, Flask-CORS |
| **AI Model**   | OpenAI Whisper Large V3 |
| **Styling**    | Custom CSS with Flexbox + Minimal UI |
| **Deployment** | GitHub Pages (Frontend), Render / Vercel / Railway (Backend) |

---

## 📦 Project Structure

audio-transcriber/
│
├── backend/
│ ├── backend.py
│ ├── requirements.txt
│ └── (optional) .env
│
├── frontend/
│ ├── public/
│ │ └── index.html
│ ├── src/
│ │ ├── App.js
│ │ ├── App.css
│ │ ├── components/
│ │ └── index.js
│ ├── package.json
│ └── README.md
│
└── README.md

✅ Backend:

You can deploy Flask backend to:

Render

Railway

Vercel (Serverless)

AWS / Azure / Google Cloud

Once deployed, update the frontend .env or config file with: 
