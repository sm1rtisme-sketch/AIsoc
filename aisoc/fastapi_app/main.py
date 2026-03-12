from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import auth, conversations, roles, groups, tasks, vulnerabilities, attack_chains, batch_tasks, config as config_api, agent, skills, knowledge, terminal, security, robot
from core.config import get_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    yield


def create_app() -> FastAPI:
    config = get_config()
    
    app = FastAPI(
        title="AISOC API",
        version=config.config.version,
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(conversations.router, prefix="/api", tags=["conversations"])
    app.include_router(roles.router, prefix="/api", tags=["roles"])
    app.include_router(groups.router, prefix="/api", tags=["groups"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(vulnerabilities.router, prefix="/api", tags=["vulnerabilities"])
    app.include_router(attack_chains.router, prefix="/api", tags=["attack_chains"])
    app.include_router(batch_tasks.router, prefix="/api", tags=["batch_tasks"])
    app.include_router(config_api.router, prefix="/api", tags=["config"])
    app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
    app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
    app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
    app.include_router(terminal.router, prefix="/api/terminal", tags=["terminal"])
    app.include_router(security.router, prefix="/api/security", tags=["security"])
    app.include_router(robot.router, prefix="/api/robot", tags=["robot"])
    
    @app.get("/api/health")
    async def health():
        return {"status": "ok", "version": config.config.version}
    
    return app


app = create_app()
