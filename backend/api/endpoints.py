import uuid
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
from services.meowy import chat_with_openai
from fastapi.responses import JSONResponse

router = APIRouter()

chat_histories = {}

class ChatRequest(BaseModel):
    user_input: str

def get_session_id(request: Request) -> str:
    """Retrieve the session ID from the cookies or generate a new UUID."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/chat/")
async def chat(request: Request, chat_request: ChatRequest, response: Response):
    """Handle user chat input and store the conversation history with a UUID session ID."""
    try:
        session_id = get_session_id(request)

        if session_id not in chat_histories:
            chat_histories[session_id] = []

        bot_reply = await chat_with_openai(chat_request.user_input)

        chat_histories[session_id].append({
            "user_input": chat_request.user_input,
            "bot_reply": bot_reply["response"]
        })

        response.set_cookie(key="session_id", value=session_id)

        return {"response": bot_reply["response"], "urls": bot_reply["urls"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/")
async def chat_history(request: Request):
    """Fetch chat history for the current session."""
    try:
        session_id = get_session_id(request)

        if session_id in chat_histories:
            return JSONResponse(content={"history": chat_histories[session_id]})
        else:
            raise HTTPException(status_code=404, detail="No chat history found for this session.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
