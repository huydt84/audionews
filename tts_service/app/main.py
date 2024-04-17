from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class Article(BaseModel):
    content: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/tts/male-north")
async def tts(article: Article):
    return FileResponse("WAV_2mb.wav")

@app.post("/tts/female-north")
async def tts(article: Article):
    return FileResponse("WAV_2mb.wav")

@app.post("/tts/male-south")
async def tts(article: Article):
    return FileResponse("WAV_2mb.wav")

@app.post("/tts/female-south")
async def tts(article: Article):
    return FileResponse("WAV_2mb.wav")

