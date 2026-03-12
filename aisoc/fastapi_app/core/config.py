import os
import yaml
from pathlib import Path
from typing import Optional, Any, Dict
from pydantic import BaseModel
from functools import lru_cache


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080


class AuthConfig(BaseModel):
    password: str = ""
    session_duration_hours: int = 12


class LogConfig(BaseModel):
    level: str = "info"
    output: str = "stdout"


class OpenAIConfig(BaseModel):
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    max_total_tokens: int = 120000


class FOFAConfig(BaseModel):
    base_url: str = "https://fofa.info/api/v1/search/all"
    email: str = ""
    api_key: str = ""


class AgentConfig(BaseModel):
    max_iterations: int = 120
    large_result_threshold: int = 102400
    result_storage_dir: str = "tmp"


class DatabaseConfig(BaseModel):
    path: str = "data/conversations.db"
    knowledge_db_path: str = "data/knowledge.db"


class SecurityConfig(BaseModel):
    tools_dir: str = "tools"
    tool_description_mode: str = "full"


class MCPConfig(BaseModel):
    enabled: bool = False
    host: str = "0.0.0.0"
    port: int = 8081
    auth_header: str = "X-MCP-Token"
    auth_header_value: str = ""


class ExternalMCPConfig(BaseModel):
    servers: Dict[str, Any] = {}


class EmbeddingConfig(BaseModel):
    provider: str = "openai"
    model: str = "text-embedding-v4"
    base_url: str = ""
    api_key: str = ""


class RetrievalConfig(BaseModel):
    top_k: int = 5
    similarity_threshold: float = 0.7
    hybrid_weight: float = 0.7


class IndexingConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 50
    max_chunks_per_item: int = 0
    max_rpm: int = 0
    rate_limit_delay_ms: int = 300
    max_retries: int = 3
    retry_delay_ms: int = 1000


class KnowledgeConfig(BaseModel):
    enabled: bool = False
    base_path: str = "knowledge_base"
    embedding: EmbeddingConfig = EmbeddingConfig()
    retrieval: RetrievalConfig = RetrievalConfig()
    indexing: IndexingConfig = IndexingConfig()


class WeComConfig(BaseModel):
    enabled: bool = False
    token: str = ""
    encoding_aes_key: str = ""
    corp_id: str = ""
    secret: str = ""
    agent_id: int = 0


class DingTalkConfig(BaseModel):
    enabled: bool = False
    client_id: str = ""
    client_secret: str = ""


class LarkConfig(BaseModel):
    enabled: bool = False
    app_id: str = ""
    app_secret: str = ""
    verify_token: str = ""


class RobotsConfig(BaseModel):
    wecom: WeComConfig = WeComConfig()
    dingtalk: DingTalkConfig = DingTalkConfig()
    lark: LarkConfig = LarkConfig()


class AppConfig(BaseModel):
    version: str = "v1.0.0"
    server: ServerConfig = ServerConfig()
    auth: AuthConfig = AuthConfig()
    log: LogConfig = LogConfig()
    openai: OpenAIConfig = OpenAIConfig()
    fofa: FOFAConfig = FOFAConfig()
    agent: AgentConfig = AgentConfig()
    database: DatabaseConfig = DatabaseConfig()
    security: SecurityConfig = SecurityConfig()
    mcp: MCPConfig = MCPConfig()
    external_mcp: ExternalMCPConfig = ExternalMCPConfig()
    knowledge: KnowledgeConfig = KnowledgeConfig()
    robots: RobotsConfig = RobotsConfig()
    skills_dir: str = "skills"
    roles_dir: str = "roles"


class Config:
    _instance: Optional['Config'] = None
    _config: AppConfig = AppConfig()
    _config_file: str = ""
    _config_dict: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config_file:
            base_dir = Path(__file__).resolve().parent.parent
            self._config_file = os.environ.get('AISOC_CONFIG_FILE', str(base_dir / 'config.yaml'))
            self._load()

    def _load(self):
        config_path = Path(self._config_file)
        if not config_path.exists():
            return

        with open(config_path, 'r', encoding='utf-8') as f:
            self._config_dict = yaml.safe_load(f) or {}

        self._config = self._parse_config(self._config_dict)

    def _parse_config(self, data: Dict[str, Any]) -> AppConfig:
        return AppConfig(
            version=data.get('version', 'v1.0.0'),
            server=ServerConfig(**data.get('server', {})),
            auth=AuthConfig(**data.get('auth', {})),
            log=LogConfig(**data.get('log', {})),
            openai=OpenAIConfig(**data.get('openai', {})),
            fofa=FOFAConfig(**data.get('fofa', {})),
            agent=AgentConfig(**data.get('agent', {})),
            database=DatabaseConfig(**data.get('database', {})),
            security=SecurityConfig(**data.get('security', {})),
            mcp=MCPConfig(**data.get('mcp', {})),
            external_mcp=ExternalMCPConfig(**data.get('external_mcp', {})),
            knowledge=KnowledgeConfig(**data.get('knowledge', {})),
            robots=RobotsConfig(**data.get('robots', {})),
            skills_dir=data.get('skills_dir', 'skills'),
            roles_dir=data.get('roles_dir', 'roles'),
        )

    def reload(self):
        self._load()

    @property
    def config(self) -> AppConfig:
        return self._config

    @property
    def raw_config(self) -> Dict[str, Any]:
        return self._config_dict

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config_dict
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value


@lru_cache()
def get_config() -> Config:
    return Config()
