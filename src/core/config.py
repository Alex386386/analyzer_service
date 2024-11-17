from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_title: str

    openai_api_key: str

    name_of_api_model: str

    access_token: str

    database_url: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: int
    db_name: str

    redis_password: int
    cache_life_period: int

    test: bool = False


settings = Settings()
