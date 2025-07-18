from fastapi import APIRouter
from fastapi import FastAPI

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}