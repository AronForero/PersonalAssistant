"""
Application configuration.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "Personal Assistant API"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # LangGraph/LLM Settings
    openai_api_key: Optional[str] = None
    langchain_api_key: Optional[str] = None
    langsmith_api_key: Optional[str] = None
    
    # Agent Settings
    default_model: str = "gpt-4.1-nano"
    default_temperature: float = 0.5
    
    # Database Settings (required from .env file)
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    
    @property
    def database_url(self) -> str:
        """Build database URL from individual components."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

