# -------- Whisper-based transcription service image --------
    FROM python:3.12-slim

    # Install ffmpeg for pydub & Whisper
    RUN apt-get update && \
        rm -rf /var/lib/apt/lists/*
    
    # Copy project
    WORKDIR /app
    COPY requirements.txt .
    

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY app/ /app
    
    CMD ["python", "app.py"]