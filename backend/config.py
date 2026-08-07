"""Configuration layer for the Flask backend."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


@dataclass(frozen=True)
class Config:
    """Central application configuration loaded from environment variables."""

    COGNODB_URI: str = os.getenv("COGNODB_URI", "bolt://localhost:7687")
    COGNODB_USERNAME: str = os.getenv("COGNODB_USERNAME", "neo4j")
    COGNODB_PASSWORD: str = os.getenv("COGNODB_PASSWORD", "password")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    PORT: int = int(os.getenv("PORT", "5000"))
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", "10"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
