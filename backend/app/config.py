from pydantic_settings import BaseSettings
from typing import List, Optional
from urllib.parse import urlparse
import os


class Settings(BaseSettings):
    # Gemini API Configuration
    GEMINI_API_KEY: str

    # Database Configuration - Supports both SQLite (dev) and PostgreSQL (prod)
    # Neon PostgreSQL: postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
    DATABASE_URL: str = "sqlite:///./seo_agent.db"

    # Application Configuration
    APP_NAME: str = "SEO Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Default to False for production

    # CORS Configuration - comma-separated URLs
    # Production: https://yourdomain.com,https://www.yourdomain.com
    # Development: http://localhost:5173,http://localhost:3000
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Reference Website (for content context)
    REFERENCE_WEBSITE: str = "https://appincoimbatore.com"
    BUSINESS_CATEGORY: str = "Digital Marketing Course in Coimbatore"
    BUSINESS_NAME: str = "Appin Technology"
    BUSINESS_LOCATION: str = "Coimbatore"

    # SEO Configuration
    MAX_RETRY_ATTEMPTS: int = 2
    MIN_VALIDATION_SCORE: int = 70

    # Optional: Add these for production monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_allowed_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    def is_postgresql(self) -> bool:
        """Check if using PostgreSQL database"""
        return self.DATABASE_URL.startswith("postgresql://") or self.DATABASE_URL.startswith("postgres://")

    def get_database_connect_args(self) -> dict:
        """Get database connection arguments based on database type"""
        if self.is_postgresql():
            # Neon PostgreSQL requires SSL
            return {
                "sslmode": "require",
                "connect_timeout": 10,
            }
        # SQLite specific args
        return {"check_same_thread": False}


settings = Settings()

# Log configuration on startup (without sensitive data)
def log_config():
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"Database: {'PostgreSQL' if settings.is_postgresql() else 'SQLite'}")
    logger.info(f"Allowed Origins: {settings.get_allowed_origins()}")