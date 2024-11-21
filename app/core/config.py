from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost/reinvent"  # Update with your DB URL
    secret_key: str = "your-secret-key"

    class Config:
        env_file = ".env"

settings = Settings()
