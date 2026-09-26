from pathlib import Path
import io

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from src.model import predict_image


project_root = Path(__file__).resolve().parents[1]
frontend_dir = project_root / 'frontend'

app = FastAPI(
    title='Coconut Disease Classification API',
    version='1.0.0'
)

app.mount('/static',
    StaticFiles(directory=frontend_dir),
    name='static')


@app.get('/')
def home():
    return FileResponse(
        frontend_dir / 'index.html')


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/predict')
async def predict(file: UploadFile = File(...)):

    if file.content_type is None or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail='Please upload a valid image file.')

    try:
        image_data = await file.read()
        image = Image.open(
            io.BytesIO(image_data) )
        image.load()

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail='The uploaded file could not be read as an image.')

    prediction, confidence = predict_image(image)

    return {'prediction': prediction,'confidence': confidence}
