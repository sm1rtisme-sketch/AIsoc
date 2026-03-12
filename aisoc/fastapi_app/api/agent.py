from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: str = None
    message: str = ""
    role: str = "default"


@router.post("/chat")
async def chat(request: ChatRequest):
    return {"message": "Chat endpoint - to be implemented"}


@router.post("/stream-chat")
async def stream_chat(request: ChatRequest):
    return {"message": "Stream chat endpoint - to be implemented"}
