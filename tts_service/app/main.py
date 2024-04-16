from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Article(BaseModel):
    content: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/tss")
async def tts(article: Article):
    return {"folder_path": "abcxyz"}
