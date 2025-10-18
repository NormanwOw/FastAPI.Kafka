from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='deploy/.env',
        env_file_encoding='utf-8'
    )

    KAFKA_HOSTS: list[str]
    KAFKA_TOPIC: str
    KAFKA_GROUP: str
    KAFKA_CLIENT_ID: str


settings = Settings()

