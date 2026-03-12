import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_config

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_database_url():
    config = get_config()
    db_path = config.config.database.path
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else "data", exist_ok=True)
    return f"sqlite:///{db_path}"


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(),
            connect_args={"check_same_thread": False}
        )
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from models import user, conversation, role, group, task, vulnerability, attack_chain, batch_task, skill_stats
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
