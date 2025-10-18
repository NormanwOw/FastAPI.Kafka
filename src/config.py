from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='deploy/.env',
        env_file_encoding='utf-8'
    )

    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_TOPIC: str
    KAFKA_GROUP: str


settings = Settings()

KAFKA_URL = f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'