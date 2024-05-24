from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

class Article(BaseModel):
    content: str
    folder_name: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/tts")
async def tts(article: Article):
    os.makedirs(f"audio/{article.folder_name}", exist_ok=True)

    with open("WAV_2mb.wav", "rb") as f:
        audio = f.read()

    with open(f"audio/{article.folder_name}/male-north.wav", "wb") as f:
        f.write(audio)
    
    with open(f"audio/{article.folder_name}/female-north.wav", "wb") as f:
        f.write(audio)

    with open(f"audio/{article.folder_name}/male-south.wav", "wb") as f:
        f.write(audio)

    with open(f"audio/{article.folder_name}/female-south.wav", "wb") as f:
        f.write(audio)

    with open(f"audio/{article.folder_name}/female-central.wav", "wb") as f:
        f.write(audio)

    return {"message": "success!"}


# @app.post("/tts/male-north")
# async def tts(article: Article):
#     return FileResponse("WAV_2mb.wav")

# @app.post("/tts/female-north")
# async def tts(article: Article):
#     return FileResponse("WAV_2mb.wav")

# @app.post("/tts/male-south")
# async def tts(article: Article):
#     return FileResponse("WAV_2mb.wav")

# @app.post("/tts/female-south")
# async def tts(article: Article):
#     return FileResponse("WAV_2mb.wav")

