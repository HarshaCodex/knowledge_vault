from fastapi import FastAPI

from knowledge_vault.routes.auth import router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Knowledge Vault API"}

app.include_router(router=router)
