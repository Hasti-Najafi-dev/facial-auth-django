from fastapi import FastAPI, UploadFile, File
import face_recognition
import io
import numpy as np

app = FastAPI()

@app.post("/encode-face/")
async def encode_face(image: UploadFile = File(...)):
    img = face_recognition.load_image_file(image.file)
    encodings = face_recognition.face_encodings(img)
    return {"encodings": encodings[0].tolist() if encodings else None}

