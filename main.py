from fastapi import FastAPI

from knowledge_vault.routes.auth import auth_router
from knowledge_vault.routes.posture import posture_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Knowledge Vault API"}

app.include_router(router=auth_router, prefix="/auth")
app.include_router(router=posture_router, prefix="/posture")