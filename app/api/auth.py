from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):

    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})

    return {"access_token": token}