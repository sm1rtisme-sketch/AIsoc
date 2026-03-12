from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
from core.database import get_db
from models.task import Task

router = APIRouter()


class CreateTaskRequest(BaseModel):
    name: str = ""


@router.get("/tasks")
async def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).limit(50).all()
    return {
        "tasks": [
            {"id": t.id, "name": t.name, "status": t.status, "progress": t.progress}
            for t in tasks
        ]
    }


@router.post("/tasks")
async def create_task(request: CreateTaskRequest, db: Session = Depends(get_db)):
    task = Task(name=request.name, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"id": task.id}


@router.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": task.id,
        "name": task.name,
        "status": task.status,
        "progress": task.progress,
        "result": task.result,
        "error": task.error,
    }


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
