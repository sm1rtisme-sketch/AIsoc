import os
import yaml
from pathlib import Path
from typing import Optional, Any, Dict
from dataclasses import dataclass, field
from django.conf import settings


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8080


@dataclass
class AuthConfig:
    password: str = ""
    session_duration_hours: int = 12


@dataclass
class LogConfig:
    level: str = "info"
    output: str = "stdout"


@dataclass
class OpenAIConfig:
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    max_total_tokens: int = 120000


@dataclass
class FOFAConfig:
    base_url: str = "https://fofa.info/api/v1/search/all"
    email: str = ""
    api_key: str = ""


@dataclass
class AgentConfig:
    max_iterations: int = 120
    large_result_threshold: int = 102400
    result_storage_dir: str = "tmp"


@dataclass
class DatabaseConfig:
    path: str = "data/conversations.db"
    knowledge_db_path: str = "data/knowledge.db"


@dataclass
class SecurityConfig:
    tools_dir: str = "tools"
    tool_description_mode: str = "full"


@dataclass
class MCPConfig:
    enabled: bool = False
    host: str = "0.0.0.0"
    port: int = 8081
    auth_header: str = "X-MCP-Token"
    auth_header_value: str = ""


@dataclass
class ExternalMCPConfig:
    servers: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingConfig:
    provider: str = "openai"
    model: str = "text-embedding-v4"
    base_url: str = ""
    api_key: str = ""


@dataclass
class RetrievalConfig:
    top_k: int = 5
    similarity_threshold: float = 0.7
    hybrid_weight: float = 0.7


@dataclass
class IndexingConfig:
    chunk_size: int = 512
    chunk_overlap: int = 50
    max_chunks_per_item: int = 0
    max_rpm: int = 0
    rate_limit_delay_ms: int = 300
    max_retries: int = 3
    retry_delay_ms: int = 1000


@dataclass
class KnowledgeConfig:
    enabled: bool = False
    base_path: str = "knowledge_base"
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    indexing: IndexingConfig = field(default_factory=IndexingConfig)


@dataclass
class WeComConfig:
    enabled: bool = False
    token: str = ""
    encoding_aes_key: str = ""
    corp_id: str = ""
    secret: str = ""
    agent_id: int = 0


@dataclass
class DingTalkConfig:
    enabled: bool = False
    client_id: str = ""
    client_secret: str = ""


@dataclass
class LarkConfig:
    enabled: bool = False
    app_id: str = ""
    app_secret: str = ""
    verify_token: str = ""


@dataclass
class RobotsConfig:
    wecom: WeComConfig = field(default_factory=WeComConfig)
    dingtalk: DingTalkConfig = field(default_factory=DingTalkConfig)
    lark: LarkConfig = field(default_factory=LarkConfig)


@dataclass
class AppConfig:
    version: str = "v1.0.0"
    server: ServerConfig = field(default_factory=ServerConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    log: LogConfig = field(default_factory=LogConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    fofa: FOFAConfig = field(default_factory=FOFAConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    external_mcp: ExternalMCPConfig = field(default_factory=ExternalMCPConfig)
    knowledge: KnowledgeConfig = field(default_factory=KnowledgeConfig)
    robots: RobotsConfig = field(default_factory=RobotsConfig)
    skills_dir: str = "skills"
    roles_dir: str = "roles"


class Config:
    _instance: Optional['Config'] = None
    _config: AppConfig = field(default_factory=AppConfig)
    _config_file: str = ""
    _config_dict: Dict[str, Any] = field(default_factory=dict)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config_file:
            self._config_file = getattr(settings, 'CONFIG_FILE', 'config.yaml')
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


def get_config() -> Config:
    return Config()
