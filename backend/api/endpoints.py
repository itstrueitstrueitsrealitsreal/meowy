import uuid
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
from backend.services.meowy import chat_with_openai
from fastapi.responses import JSONResponse

router = APIRouter()

# In-memory chat histories, keyed by session UUID (in practice, store this in a database)
chat_histories = {}

class ChatRequest(BaseModel):
    user_input: str

def get_session_id(request: Request) -> str:
    """Retrieve the session ID from the cookies or generate a new UUID."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        # Generate a new session ID using UUID
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/chat/")
async def chat(request: Request, chat_request: ChatRequest, response: Response):
    """Handle user chat input and store the conversation history with a UUID session ID."""
    try:
        # Get or generate a session ID
        session_id = get_session_id(request)

        # Retrieve or create a new chat history for the session
        if session_id not in chat_histories:
            chat_histories[session_id] = []

        # Process the user's input using the chat_with_openai function
        bot_reply = await chat_with_openai(chat_request.user_input)

        # Store the chat message and bot's reply in the session history
        chat_histories[session_id].append({
            "user_input": chat_request.user_input,
            "bot_reply": bot_reply["response"]
        })

        # Set the session UUID cookie if it's new
        response.set_cookie(key="session_id", value=session_id)

        # Return the bot's reply
        return {"response": bot_reply["response"], "urls": bot_reply["urls"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/")
async def chat_history(request: Request):
    """Fetch chat history for the current session."""
    try:
        # Get the session ID from the cookie
        session_id = get_session_id(request)

        # Check if chat history exists for the session
        if session_id in chat_histories:
            return JSONResponse(content={"history": chat_histories[session_id]})
        else:
            raise HTTPException(status_code=404, detail="No chat history found for this session.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
