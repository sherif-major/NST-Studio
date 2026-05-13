from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from uuid import uuid4

from NST import run_style_transfer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONTENT_DIR = os.path.join(BASE_DIR, "data/content-images")
STYLE_DIR = os.path.join(BASE_DIR, "data/style-images")
OUTPUT_DIR = os.path.join(BASE_DIR, "data/output-images")

os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(STYLE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Neural Style Transfer API çalışıyor"}


@app.get("/styles")
def get_styles():
    styles = []

    for filename in os.listdir(STYLE_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            styles.append({
                "name": filename,
                "url": f"http://localhost:8000/style-image/{filename}"
            })

    return styles


@app.get("/style-image/{filename}")
def get_style_image(filename: str):
    path = os.path.join(STYLE_DIR, filename)
    return FileResponse(path)


@app.post("/style-transfer")
async def style_transfer(
    content: UploadFile = File(...),
    style_name: str = Form(...)
):
    content_filename = f"{uuid4()}_{content.filename}"
    content_path = os.path.join(CONTENT_DIR, content_filename)

    with open(content_path, "wb") as buffer:
        shutil.copyfileobj(content.file, buffer)

    output_path = run_style_transfer(content_filename, style_name)

    return FileResponse(
        output_path,
        media_type="image/jpeg",
        filename="result.jpg"
    )