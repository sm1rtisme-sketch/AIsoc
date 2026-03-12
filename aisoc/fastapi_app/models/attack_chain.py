import uuid
from sqlalchemy import Column, String, DateTime, Integer, Text, JSON
from datetime import datetime
from core.database import Base


class AttackChain(Base):
    __tablename__ = "attack_chains"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(500), default="")
    description = Column(Text, default="")
    steps = Column(JSON, default=list)
    status = Column(String(50), default="pending")
    created_by_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BatchTask(Base):
    __tablename__ = "batch_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(500), default="")
    target_list = Column(JSON, default=list)
    tool_name = Column(String(200), default="")
    tool_config = Column(JSON, default=dict)
    status = Column(String(50), default="pending")
    progress = Column(Integer, default=0)
    total = Column(Integer, default=0)
    results = Column(JSON, default=list)
    created_by_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SkillStats(Base):
    __tablename__ = "skill_stats"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    skill_name = Column(String(200), default="")
    tool_name = Column(String(200), default="")
    call_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    total_duration = Column(Integer, default=0)
    last_called = Column(DateTime, nullable=True)
