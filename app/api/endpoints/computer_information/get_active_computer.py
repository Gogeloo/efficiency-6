from fastapi import APIRouter


router = APIRouter()

@router.get("/active-computer")
async def get_active_computers():
    return "I am a response:"
    