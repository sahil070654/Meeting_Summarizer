🧠 Meeting Summarizer

A Flask-based AI Web App that transcribes long meeting audio files and generates clear, concise summaries — fast, secure, and easy to use.


Backend: Railway | Frontend: GitHub Pages / Local

🚀 Overview

Meeting Summarizer is a web-based tool that:

Converts long meeting recordings (up to ~30 minutes) into text.

Generates structured and concise summaries using AI.

Works with various audio formats (.mp3, .wav, .m4a, etc.).

Runs completely in the browser for uploads — secure and private.

🧩 Features

✅ Transcription using Whisper (Groq API)
✅ Summarization using LLaMA 3.1 (Groq API)
✅ Supports large audio files (up to 30 min)
✅ Fast and secure — no data is stored
✅ Simple, responsive, and elegant UI
✅ Deployed backend on Railway
✅ Frontend hosted via GitHub Pages

🛠️ Tech Stack
Layer	Technologies Used
Frontend	HTML5, CSS3, JavaScript
Backend	Flask, Python
AI Models	Whisper Large V3 (Speech-to-Text), LLaMA 3.1 8B Instant (Summarization)
Deployment	Railway (Backend), GitHub Pages (Frontend)
Other Tools	FFmpeg (Audio Splitting), Requests, Flask-CORS
🧪 Project Structure
meeting-summarizer/
│
├── backend.py             # Flask backend for transcription & summarization
├── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html         # Main UI
│   ├── style.css          # Frontend design
│   └── script.js          # API integration logic
│
└── README.md              # Project documentation

⚙️ Setup Instructions
🧩 Prerequisites

Python 3.10+

FFmpeg installed (sudo apt install ffmpeg)

Groq API Key (get from groq.com
)

Git & basic terminal access

🖥️ Backend Setup (Flask)

Clone the repository:

git clone https://github.com/<your-username>/meeting-summarizer.git
cd meeting-summarizer


Create a virtual environment & install dependencies:

pip install -r requirements.txt


Set your Groq API Key (Mac/Linux):

export GROQ_API_KEY="your_api_key_here"


(For Windows PowerShell: setx GROQ_API_KEY "your_api_key_here")

Run the Flask backend:

python backend.py


The backend will start at:
➡️ http://127.0.0.1:5000

🌐 Frontend Setup (Local or GitHub Pages)
Option 1 — Local:

Open the frontend/index.html file directly in your browser.

Update the backend URL in script.js:

const backendURL = "https://meetingsummarizer-production.up.railway.app/summarize_audio";


Upload an audio file and click “🎤 Transcribe & Summarize”.

Option 2 — GitHub Pages:

Push the frontend/ folder to a GitHub repo.

Go to Settings → Pages → Deploy from Branch → /frontend folder.

Open your live site using the GitHub Pages URL.

☁️ Backend Deployment (Railway)

Create a new project on Railway.app
.

Connect your GitHub repository.

Add environment variable:

GROQ_API_KEY = your_api_key_here


Deploy — Railway will automatically assign a backend URL like:

https://meetingsummarizer-production.up.railway.app

🧠 How It Works

Upload your meeting audio (up to 30 minutes).

The backend splits the audio using ffmpeg.

Each chunk is transcribed using the Whisper model.

The combined transcript is then summarized using LLaMA 3.1.

The results are sent back to the frontend and displayed neatly.

📸 Example Output

Transcript:

"Good morning everyone. Today we discussed the Q4 roadmap and the new product launch schedule..."

Summary:

Team discussed Q4 roadmap and deadlines.

Product launch set for next quarter.

Budget approval pending from finance.

💡 Future Enhancements

Add download as PDF for summaries

Multi-language transcription

Speaker identification

Cloud storage integration (Google Drive)

👤 Author

Sahil
🎓 B.Tech CSE | VIT-AP University
💼 Passionate about Machine Learning, AI, and Full Stack Development
🌐 GitHub
 | LinkedIn

📄 License

This project is licensed under the MIT License — feel free to use and modify with attribution.
