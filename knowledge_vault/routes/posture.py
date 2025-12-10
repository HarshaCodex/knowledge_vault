from fastapi import APIRouter, File, UploadFile

from knowledge_vault.utils.posture_util import extract_landmarks, detect_posture

posture_router = APIRouter()

@posture_router.post("/analyze-posture")
async def posture_analyze(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        posture_landmarks = extract_landmarks(image_bytes)
        return detect_posture(posture_landmarks)
    except Exception as e:
        return {"message": str(e)}