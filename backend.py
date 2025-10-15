# backend.py
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import math
import os
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

# --- CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Keep your key in env variables
MODEL_TRANSCRIBE = "whisper-large-v3"
MODEL_SUMMARY = "llama-3.1-8b-instant"  # supported model

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- Optional: ngrok for Colab testing ---
if os.environ.get("COLAB_TUNNEL") == "1":
    try:
        from pyngrok import ngrok
        port = 5000
        public_url = ngrok.connect(port)
        print(f"✅ Public ngrok URL for Colab: {public_url}")
    except Exception as e:
        print("Ngrok not running:", e)

# --- Home Route ---
@app.route("/")
def home():
    return "<h3>✅ Meeting Summarizer Backend Running</h3>"

# --- Helper: split audio into 1-min chunks ---
def split_audio(file_path, chunk_length_ms=60*1000):
    audio = AudioSegment.from_file(file_path)
    chunks = []
    total_chunks = math.ceil(len(audio) / chunk_length_ms)
    for i in range(total_chunks):
        start = i * chunk_length_ms
        end = start + chunk_length_ms
        chunk = audio[start:end]
        chunk_name = f"chunk_{i}.mp3"
        chunk.export(chunk_name, format="mp3")
        chunks.append(chunk_name)
    return chunks

# --- Main Route: Transcribe + Summarize ---
@app.route("/summarize_audio", methods=["POST"])
def summarize_audio():
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]

    # Save temporary file
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_file.save(temp_audio.name)

    # Split audio into chunks (1 minute each)
    chunk_files = split_audio(temp_audio.name, chunk_length_ms=60*1000)

    all_text = ""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    # Transcribe each chunk
    for cf in chunk_files:
        with open(cf, "rb") as f:
            files = {"file": (cf, f, "audio/mpeg")}
            resp = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data={"model": MODEL_TRANSCRIBE},
            )
        if resp.status_code == 200:
            all_text += resp.json().get("text", "") + " "
        else:
            print("Chunk failed:", resp.text)
        os.remove(cf)

    # Summarize the combined transcript
    summary_payload = {
        "model": MODEL_SUMMARY,
        "messages": [
            {"role": "system", "content": "Summarize this long meeting clearly in bullet points."},
            {"role": "user", "content": all_text},
        ],
    }

    sresp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={**headers, "Content-Type": "application/json"},
        json=summary_payload,
    )

    if sresp.status_code != 200:
        return jsonify({"error": "Summary failed", "details": sresp.text}), 500

    summary = sresp.json()["choices"][0]["message"]["content"]
    return jsonify({"transcript": all_text, "summary": summary})

# --- Run Flask App ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env variable
    app.run(host="0.0.0.0", port=port)
