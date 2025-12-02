import os
from fastapi import APIRouter, File, UploadFile

posture_router = APIRouter()

@posture_router.post("/analyze-posture")
async def posture_analyze(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()

        if not os.path.exists("uploads"):
            os.mkdir("uploads")
            
        with open(f"uploads/{image.filename}", "wb") as f:
            f.write(image_bytes)

        return {"message": "Image uploaded and saved successfully."}
    except Exception as e:
        return {"message": str(e)}