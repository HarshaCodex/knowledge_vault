from fastapi import APIRouter
from knowledge_vault.utils.security import create_user
from knowledge_vault.models.schemas import UserCreate

router = APIRouter()

@router.post("/auth/add-user")
def add_user(user: UserCreate):
    created = create_user(user.username, user.email, user.password)
    if created:
        return {"message": "User created successfully"}
    else:
        return {"message": "User creation failed"}
