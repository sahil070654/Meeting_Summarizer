# backend.py
# -*- coding: utf-8 -*-

import os
import subprocess
import glob
from tempfile import NamedTemporaryFile
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIG ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Keep your key in environment variables
MODEL_TRANSCRIBE = "whisper-large-v3"
MODEL_SUMMARY = "llama-3.1-8b-instant"  # supported model

# --- Flask App ---
app = Flask(__name__)
CORS(app)

# --- Home Route ---
@app.route("/")
def home():
    return "<h3>✅ Meeting Summarizer Backend Running</h3>"

# --- Helper: Split audio using ffmpeg ---
def split_audio_ffmpeg(file_path, chunk_length_sec=60):
    """
    Splits audio into chunks using ffmpeg.
    Returns list of chunk file names.
    """
    # Remove old chunks
    for f in glob.glob("chunk_*.mp3"):
        os.remove(f)

    # FFmpeg command
    cmd = [
        "ffmpeg", "-y", "-i", file_path,
        "-f", "segment",
        "-segment_time", str(chunk_length_sec),
        "-c", "copy",
        "chunk_%03d.mp3"
    ]
    subprocess.run(cmd, check=True)

    # Return sorted list of chunk files
    return sorted(glob.glob("chunk_*.mp3"))

# --- Main Route: Transcribe + Summarize ---
@app.route("/summarize_audio", methods=["POST"])
def summarize_audio():
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]

    # Save temporary file
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_file.save(temp_audio.name)
        temp_file_path = temp_audio.name

    try:
        # Split audio into chunks
        chunk_files = split_audio_ffmpeg(temp_file_path, chunk_length_sec=60)

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

    finally:
        # Clean up temp audio file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# --- Run Flask App ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT environment variable
    app.run(host="0.0.0.0", port=port)
