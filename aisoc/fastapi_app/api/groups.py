from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Any
from core.database import get_db
from models.role import Group

router = APIRouter()


class CreateGroupRequest(BaseModel):
    name: str
    description: str = ""


@router.get("/groups")
async def list_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return {
        "groups": [
            {"id": g.id, "name": g.name, "description": g.description}
            for g in groups
        ]
    }


@router.post("/groups")
async def create_group(request: CreateGroupRequest, db: Session = Depends(get_db)):
    group = Group(name=request.name, description=request.description)
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"id": group.id, "name": group.name}


@router.get("/groups/{group_id}")
async def get_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
    }


@router.delete("/groups/{group_id}")
async def delete_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(group)
    db.commit()
    return {"message": "Deleted"}
