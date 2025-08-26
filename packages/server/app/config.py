from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: str
    face_model_path: str

    class Config:
        env_file = ".env"

settings = Settings()