from passlib.context import CryptContext
from knowledge_vault.utils.database import db as SessionLocal
from knowledge_vault.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(username, email, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            print(f"{username} already exists!!!")
            return False

        hashed_password = pwd_context.hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"{username} created successfully!!!")
        return True
    finally:
        db.close()
