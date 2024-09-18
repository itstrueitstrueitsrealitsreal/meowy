from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.meowy import chat_with_openai

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str

@router.post("/chat/")
async def chat(request: ChatRequest):
    """Handle user chat input."""
    try:
        bot_reply = await chat_with_openai(request.user_input)
        return {"response": bot_reply["response"], "urls": bot_reply["urls"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
