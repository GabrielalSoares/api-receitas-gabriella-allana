from pydantic_settings import BaseSettings, settingsConfigDict


class Settings(BaeSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_fle_encoding='utf-8'
    )

    DATABASE_URL: str