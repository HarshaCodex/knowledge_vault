from fastapi import APIRouter, File, UploadFile

from knowledge_vault.utils.posture_util import extract_landmarks

posture_router = APIRouter()

@posture_router.post("/analyze-posture")
async def posture_analyze(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        extract_landmarks(image_bytes)

        return {"message": "Image uploaded and saved successfully."}
    except Exception as e:
        return {"message": str(e)}