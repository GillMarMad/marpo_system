from pydantic import BaseSettings
class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD = "marpo123"
    POSTGRES_SERVER: str = "192.168.1.101"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "marpo_db"
    PROJECT_NAME: str = "Marpo System"
    API_STR : str = "/api"

settings = Settings()