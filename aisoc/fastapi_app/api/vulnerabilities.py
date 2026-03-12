from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
from core.database import get_db
from models.vulnerability import Vulnerability

router = APIRouter()


class CreateVulnerabilityRequest(BaseModel):
    name: str = ""
    severity: str = "info"
    description: str = ""
    url: str = ""
    parameters: Dict[str, Any] = {}
    payload: str = ""
    evidence: str = ""


@router.get("/vulnerabilities")
async def list_vulnerabilities(db: Session = Depends(get_db)):
    vulns = db.query(Vulnerability).limit(50).all()
    return {
        "vulnerabilities": [
            {"id": v.id, "name": v.name, "severity": v.severity, "url": v.url}
            for v in vulns
        ]
    }


@router.post("/vulnerabilities")
async def create_vulnerability(request: CreateVulnerabilityRequest, db: Session = Depends(get_db)):
    vuln = Vulnerability(
        name=request.name,
        severity=request.severity,
        description=request.description,
        url=request.url,
        parameters=request.parameters,
        payload=request.payload,
        evidence=request.evidence,
    )
    db.add(vuln)
    db.commit()
    db.refresh(vuln)
    return {"id": vuln.id}


@router.get("/vulnerabilities/{vuln_id}")
async def get_vulnerability(vuln_id: str, db: Session = Depends(get_db)):
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": vuln.id,
        "name": vuln.name,
        "severity": vuln.severity,
        "description": vuln.description,
        "url": vuln.url,
    }


@router.delete("/vulnerabilities/{vuln_id}")
async def delete_vulnerability(vuln_id: str, db: Session = Depends(get_db)):
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(vuln)
    db.commit()
    return {"message": "Deleted"}
