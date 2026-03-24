from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'AvaliaZap API'
    api_prefix: str = '/api/v1'

    database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/avaliazap'

    jwt_secret: str = 'change-me'
    jwt_algorithm: str = 'HS256'
    jwt_exp_minutes: int = 60 * 24

    whatsapp_access_token: str = ''
    whatsapp_phone_number_id: str = ''
    whatsapp_api_version: str = 'v21.0'

    google_api_key: str = ''


settings = Settings()
