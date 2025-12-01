from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter
import jwt

from knowledge_vault.models.user import User
from knowledge_vault.utils.security import create_user, login
from knowledge_vault.models.schemas import Token, UserCreate, UserResponse, UserLogin
from knowledge_vault.utils.database import db as SessionLocal

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

auth_router = APIRouter()

@auth_router.post("/add-user")
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

@auth_router.post("/login")
def login_user(user: UserLogin):
    try:
        login_user = login(user.email, user.password)
        if login_user:
            jwt_request = {
                "sub": str(login_user.id),
                "username": login_user.username,
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(jwt_request, SECRET_KEY, algorithm=ALGORITHM)
            return Token(access_token=token, token_type="bearer")
        else:
            return {"message": "Login failed"}
    except Exception as e:
        return {"message": str(e)}