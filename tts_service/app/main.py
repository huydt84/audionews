from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

from models import TTS
from cleaner import NewsCleaner

class Article(BaseModel):
    content: str
    folder_name: str

# app = FastAPI()

# model = {}

# @app.on_event("startup")
# async def load_model():
#     print("start")
#     model["male-north"] = TTS("models/nam_bac/model.onnx", "models/nam_bac/config.json")
#     model["male-south"] = TTS("models/nam_nam/model.onnx", "models/nam_nam/config.json")
#     model["female-north"] = TTS("models/nu_bac/model.onnx", "models/nu_bac/config.json")
#     model["female-south"] = TTS("models/nu_nam/model.onnx", "models/nu_nam/config.json")
#     model["female-central"] = TTS("models/nu_trung/model.onnx", "models/nu_trung/config.json")
#     print("Model setup completed!")

# @app.on_event("shutdown")
# async def clear_model():
#     print("shutdown")
#     model.clear()
    
model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    model["male-north"] = TTS("models/nam_bac/model.onnx", "models/nam_bac/config.json")
    model["male-south"] = TTS("models/nam_nam/model.onnx", "models/nam_nam/config.json")
    model["female-north"] = TTS("models/nu_bac/model.onnx", "models/nu_bac/config.json")
    model["female-south"] = TTS("models/nu_nam/model.onnx", "models/nu_nam/config.json")
    model["female-central"] = TTS("models/nu_trung/model.onnx", "models/nu_trung/config.json")
    model["cleaner"] = NewsCleaner("foreign_word.txt")
    print("Model setup completed!")
    yield
    print("shutdown")
    model.clear()

app = FastAPI(lifespan=lifespan)

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

@app.post("/tts-real")
async def tts_real(article: Article):
    os.makedirs(f"audio/{article.folder_name}", exist_ok=True)

    if len(article.content.strip()) == 0:
        return {"message": "error: no content to generate audio!"}

    text = model["cleaner"].cleaner(article.content)

    model["male-north"].inference(text, f"audio/{article.folder_name}/male-north.wav")
    model["male-south"].inference(text, f"audio/{article.folder_name}/male-south.wav")
    model["female-north"].inference(text, f"audio/{article.folder_name}/female-north.wav")
    model["female-south"].inference(text, f"audio/{article.folder_name}/female-south.wav")
    model["female-central"].inference(text, f"audio/{article.folder_name}/female-central.wav")
    
    return {"message": "success!"}



