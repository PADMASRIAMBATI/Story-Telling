from pydantic_settings import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "StoryGenie"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-Powered Multi-Lingual Storytelling Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    MONGODB_URI: str
    DATABASE_NAME: str = "storygenie"
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security
    SECURITY_PASSWORD_MIN_LENGTH: int = 6
    SECURITY_BCRYPT_ROUNDS: int = 12
    
    # AI Models
    HUGGINGFACE_API_KEY: Optional[str] = None
    NLP_API_MODEL: str = "google/gemma-7b-it"
    MODEL_CACHE_DIR: str = "./ml_models_cache"
    MODEL_TIMEOUT_SECONDS: int = 60
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()