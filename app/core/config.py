from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "dev123"
    algorithm: str = "HS256"
    access_token_expire_hours: int = 1
    redis_host: str = "redis"
    redis_port: int = 6379
    model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

settings = Settings()