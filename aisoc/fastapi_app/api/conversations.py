from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from core.database import get_db
from models.conversation import Conversation, Message
from models.user import User

router = APIRouter()


class CreateConversationRequest(BaseModel):
    title: str = "New Conversation"


class UpdateConversationRequest(BaseModel):
    title: str


class MessageCreate(BaseModel):
    role: str = "user"
    content: str = ""
    tool_calls: List[Any] = []
    tool_results: List[Any] = []


@router.get("/conversations")
async def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).limit(50).all()
    return {
        "conversations": [
            {"id": c.id, "title": c.title, "created_at": c.created_at.isoformat(), "updated_at": c.updated_at.isoformat()}
            for c in convs
        ]
    }


@router.post("/conversations")
async def create_conversation(request: CreateConversationRequest, db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        user = User(username="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    conv = Conversation(user_id=user.id, title=request.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"id": conv.id, "title": conv.title}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat(),
        "updated_at": conv.updated_at.isoformat(),
    }


@router.put("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, request: UpdateConversationRequest, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    conv.title = request.title
    db.commit()
    return {"message": "Updated"}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(conv)
    db.commit()
    return {"message": "Deleted"}


@router.get("/conversations/{conversation_id}/messages")
async def list_messages(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    msgs = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "tool_calls": m.tool_calls,
                "tool_results": m.tool_results,
                "created_at": m.created_at.isoformat(),
            }
            for m in msgs
        ]
    }


@router.post("/conversations/{conversation_id}/messages")
async def create_message(conversation_id: str, request: MessageCreate, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    msg = Message(
        conversation_id=conversation_id,
        role=request.role,
        content=request.content,
        tool_calls=request.tool_calls,
        tool_results=request.tool_results,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"id": msg.id}
