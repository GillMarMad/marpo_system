from pydantic import BaseSettings
class Settings(BaseSettings):
    POSTGRES_USER: str = "marpo"
    POSTGRES_PASSWORD = "marpodb2023"
    POSTGRES_SERVER: str = "192.168.1.92"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "marpo_db"
    PROJECT_NAME: str = "Marpo System"
    API_STR : str = "/api"

settings = Settings()