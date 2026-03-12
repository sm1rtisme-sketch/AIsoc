from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Any
from core.database import get_db
from models.role import Role

router = APIRouter()


class CreateRoleRequest(BaseModel):
    name: str
    description: str = ""
    system_prompt: str = ""
    tools: List[Any] = []
    is_default: bool = False


class UpdateRoleRequest(BaseModel):
    name: str = None
    description: str = None
    system_prompt: str = None
    tools: List[Any] = None
    is_default: bool = None


@router.get("/roles")
async def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return {
        "roles": [
            {"id": r.id, "name": r.name, "description": r.description, "is_default": r.is_default}
            for r in roles
        ]
    }


@router.post("/roles")
async def create_role(request: CreateRoleRequest, db: Session = Depends(get_db)):
    role = Role(
        name=request.name,
        description=request.description,
        system_prompt=request.system_prompt,
        tools=request.tools,
        is_default=request.is_default,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"id": role.id, "name": role.name}


@router.get("/roles/{role_id}")
async def get_role(role_id: str, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "system_prompt": role.system_prompt,
        "tools": role.tools,
        "is_default": role.is_default,
    }


@router.put("/roles/{role_id}")
async def update_role(role_id: str, request: UpdateRoleRequest, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Not found")
    if request.name is not None:
        role.name = request.name
    if request.description is not None:
        role.description = request.description
    if request.system_prompt is not None:
        role.system_prompt = request.system_prompt
    if request.tools is not None:
        role.tools = request.tools
    if request.is_default is not None:
        role.is_default = request.is_default
    db.commit()
    return {"message": "Updated"}


@router.delete("/roles/{role_id}")
async def delete_role(role_id: str, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(role)
    db.commit()
    return {"message": "Deleted"}
