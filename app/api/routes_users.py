from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return {"id": 1, "name": "Bob"}