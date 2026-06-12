from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str
    database_pool_size: int = 5
    database_max_overflow: int = 5
    database_pool_recycle: int = 300
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # Object Storage
    storage_provider: str = "local"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "auto"
    aws_bucket_name: str = "ahluwalia-growth-os"
    r2_account_id: str = ""
    
    # Application
    app_name: str = "Ahluwalia Growth OS"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # CORS
    cors_origins: str = "http://localhost:3000"
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
