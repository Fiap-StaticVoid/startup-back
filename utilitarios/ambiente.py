from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigsAmbiente(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ASYNC_PG_ENGINE: str
    PG_ENGINE: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_DATABASE: str
    PG_SCHEMA: str

    @property
    def PG_URL(self) -> str:
        return (
            f"postgresql+{self.ASYNC_PG_ENGINE}://"
            f"{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}"
        )
