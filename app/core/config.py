from pydantic import BaseSettings
class Settings(BaseSettings):
    POSTGRES_USER: str = "marpo"
    POSTGRES_PASSWORD = "marpo9711251"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "marpo_db"
    PROJECT_NAME: str = "Marpo System"
    API_STR : str = "/api"

settings = Settings()