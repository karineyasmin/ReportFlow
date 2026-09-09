from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    PROJECT_NAME: str = Field(default="ReportFlow")
    API_V1_STR: str = Field(default="/api/v1")

    # Keycloak
    KEYCLOAK_SERVER_URL: str = Field(default="http://localhost:8080")
    KEYCLOAK_PUBLIC_URL: str = Field(default="http://localhost:8080")
    KEYCLOAK_REALM: str = Field(default="ReportFlowRealm")
    KEYCLOAK_CLIENT_ID: str = Field(default="reportflow-backend")
    KEYCLOAK_CLIENT_SECRET: str = Field(default="")
    KEYCLOAK_CERTS_URL: str = Field(default="")

    # Celery & Redis
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
