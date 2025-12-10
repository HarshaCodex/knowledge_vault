from fastapi import APIRouter, File, UploadFile
from fastapi.params import Depends

from knowledge_vault.models.user import User
from knowledge_vault.routes.auth import get_current_user
from knowledge_vault.utils.posture_util import extract_landmarks, detect_posture

posture_router = APIRouter()

@posture_router.post("/analyze-posture")
async def posture_analyze(image: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        image_bytes = await image.read()
        posture_landmarks = extract_landmarks(image_bytes)
        return detect_posture(posture_landmarks)
    except Exception as e:
        return {"message": str(e)}