import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(150), unique=True, nullable=False)
    role = Column(String(50), default="default")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    password_hash = Column(String(255), nullable=True)
    
    conversations = relationship("Conversation", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    vulnerabilities = relationship("Vulnerability", back_populates="created_by_user")
    attack_chains = relationship("AttackChain", back_populates="created_by_user")
    batch_tasks = relationship("BatchTask", back_populates="created_by_user")
