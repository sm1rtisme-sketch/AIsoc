from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from core.database import get_db
from models.attack_chain import BatchTask

router = APIRouter()


class CreateBatchTaskRequest(BaseModel):
    name: str = ""
    target_list: List[str] = []
    tool_name: str = ""
    tool_config: Dict[str, Any] = {}


@router.get("/batch-tasks")
async def list_batch_tasks(db: Session = Depends(get_db)):
    tasks = db.query(BatchTask).limit(50).all()
    return {
        "batch_tasks": [
            {"id": t.id, "name": t.name, "status": t.status, "progress": t.progress, "total": t.total}
            for t in tasks
        ]
    }


@router.post("/batch-tasks")
async def create_batch_task(request: CreateBatchTaskRequest, db: Session = Depends(get_db)):
    task = BatchTask(
        name=request.name,
        target_list=request.target_list,
        tool_name=request.tool_name,
        tool_config=request.tool_config,
        total=len(request.target_list),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"id": task.id}


@router.get("/batch-tasks/{task_id}")
async def get_batch_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(BatchTask).filter(BatchTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": task.id,
        "name": task.name,
        "status": task.status,
        "progress": task.progress,
        "total": task.total,
        "results": task.results,
    }


@router.delete("/batch-tasks/{task_id}")
async def delete_batch_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(BatchTask).filter(BatchTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
