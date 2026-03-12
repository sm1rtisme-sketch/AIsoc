import uuid
from sqlalchemy import Column, String, DateTime, Integer, Text, JSON
from datetime import datetime
from core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    name = Column(String(500), default="")
    status = Column(String(20), default="pending")
    progress = Column(Integer, default=0)
    result = Column(JSON, default=dict)
    error = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
