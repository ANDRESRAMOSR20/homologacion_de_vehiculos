import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./sql_app.db")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SIM_THRESHOLD: float = float(os.getenv("SIM_THRESHOLD", "0.8"))
    VECTOR_INDEX_PATH: str = os.getenv("VECTOR_INDEX_PATH", "src/vector_store/index.faiss")

    class Config:
        env_file = ".env"

settings = Settings()
