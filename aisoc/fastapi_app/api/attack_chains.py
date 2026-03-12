from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Any
from core.database import get_db
from models.attack_chain import AttackChain

router = APIRouter()


class CreateAttackChainRequest(BaseModel):
    name: str = ""
    description: str = ""
    steps: List[Any] = []


@router.get("/attack-chains")
async def list_attack_chains(db: Session = Depends(get_db)):
    chains = db.query(AttackChain).limit(50).all()
    return {
        "attack_chains": [
            {"id": c.id, "name": c.name, "status": c.status}
            for c in chains
        ]
    }


@router.post("/attack-chains")
async def create_attack_chain(request: CreateAttackChainRequest, db: Session = Depends(get_db)):
    chain = AttackChain(
        name=request.name,
        description=request.description,
        steps=request.steps,
        status="pending",
    )
    db.add(chain)
    db.commit()
    db.refresh(chain)
    return {"id": chain.id}


@router.get("/attack-chains/{chain_id}")
async def get_attack_chain(chain_id: str, db: Session = Depends(get_db)):
    chain = db.query(AttackChain).filter(AttackChain.id == chain_id).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": chain.id,
        "name": chain.name,
        "description": chain.description,
        "steps": chain.steps,
        "status": chain.status,
    }


@router.delete("/attack-chains/{chain_id}")
async def delete_attack_chain(chain_id: str, db: Session = Depends(get_db)):
    chain = db.query(AttackChain).filter(AttackChain.id == chain_id).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(chain)
    db.commit()
    return {"message": "Deleted"}
