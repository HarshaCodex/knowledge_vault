import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from knowledge_vault.models.schemas import Token, UserCreate, UserResponse
from knowledge_vault.models.user import User
from knowledge_vault.utils.database import db as SessionLocal
from knowledge_vault.utils.security import create_user, login

load_dotenv()

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        login_user = login(email=form_data.username, password=form_data.password)
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

def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).get(user_data.get("sub"))
        if user is None:
            raise Exception("User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")