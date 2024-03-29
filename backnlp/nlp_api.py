import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from nlp import generate_text, text_to_speech


PORT_API = 8000  # port utiliser par uvicorn

app = FastAPI()

origins = ["http://localhost:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/forecast")
async def forecast(city: str, date: str, hour: int = None):
    try:
        text = generate_text(city, date, hour) 
        print(f"texte généré:{text}")
        audio_file = text_to_speech(text, city, date, hour)
        audio_path = f"audio/{audio_file}"
        print(f"audio généré:{audio_path}")
        return FileResponse(audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
