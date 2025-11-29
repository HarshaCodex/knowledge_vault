from fastapi import APIRouter

from knowledge_vault.models.user import User
from knowledge_vault.utils.security import create_user, login
from knowledge_vault.models.schemas import UserCreate, UserResponse, UserLogin
from knowledge_vault.utils.database import db as SessionLocal

router = APIRouter()

@router.post("/auth/add-user")
def add_user(user: UserCreate):
    try:
        db = SessionLocal()
        created = create_user(user.username, user.email, user.password)
        if created:
            created_user = db.query(User).filter(User.username == user.username).first()
            return UserResponse(id=created_user.id, username=created_user.username, email=created_user.email, created_at=created_user.created_at)
        else:
            return {"message": "User creation failed"}
    except Exception as e:
        return {"message": str(e)}

@router.post("/auth/login")
def login_user(user: UserLogin):
    try:
        login_success = login(user.email, user.password)
        if login_success:
            return {"message": "Login successful"}
        else:
            return {"message": "Login failed"}
    except Exception as e:
        return {"message": str(e)}