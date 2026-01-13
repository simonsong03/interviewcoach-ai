from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    # Ensure uploads/ directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Get the extension (preserve original, e.g., .webm, .wav, .mp3)
    original_filename = file.filename
    _, ext = os.path.splitext(original_filename)
    if not ext:
        ext = ".bin"
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return JSONResponse({
        "original_filename": original_filename,
        "saved_file_path": file_path
    })