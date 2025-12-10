from fastapi import APIRouter, File, UploadFile

from fastapi.params import Depends

from knowledge_vault.models.posture import Posture
from knowledge_vault.models.user import User
from knowledge_vault.routes.auth import get_current_user
from knowledge_vault.utils.posture_util import extract_landmarks, detect_posture
from knowledge_vault.utils.database import db as SessionLocal

posture_router = APIRouter()

@posture_router.post("/analyze-posture")
async def posture_analyze(image: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        db = SessionLocal()
        image_bytes = await image.read()
        posture_landmarks = extract_landmarks(image_bytes)
        posture = detect_posture(posture_landmarks, current_user)

        if posture:
            saved_posture = db.query(Posture).filter(Posture.user_id == posture.user_id).first()
            if not saved_posture:
                db.add(posture)
                db.commit()
                db.refresh(posture)
                return posture
            else:
                saved_posture.score = posture.score
                saved_posture.status = posture.status
                saved_posture.issues = posture.issues
                db.commit()
                db.refresh(saved_posture)
                return saved_posture
        else:
            raise Exception("Posture analysis failed")

    except Exception as e:
        return {"message": str(e)}