from fastapi import APIRouter
from core.config import get_config

router = APIRouter()


@router.get("/config")
async def get_config_endpoint():
    config = get_config()
    return {
        "version": config.config.version,
        "server": {"host": config.config.server.host, "port": config.config.server.port},
        "auth": {"session_duration_hours": config.config.auth.session_duration_hours},
        "openai": {
            "base_url": config.config.openai.base_url,
            "model": config.config.openai.model,
        },
    }


@router.get("/openapi.json")
async def get_openapi_spec():
    config = get_config()
    return {
        "openapi": "3.0.0",
        "info": {"title": "AISOC API", "version": config.config.version},
        "paths": {},
    }
