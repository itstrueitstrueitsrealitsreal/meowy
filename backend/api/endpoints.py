from fastapi import APIRouter
from app.services.openai_service import chat_with_openai
from app.services.cat_service import get_cat_image

router = APIRouter()

@router.post("/chat/")
async def chat(user_input: str):
    return await chat_with_openai(user_input)

@router.get("/cat/")
async def cat(breed: str = None):
    return await get_cat_image(breed)
