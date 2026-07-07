"""Configuracion de la aplicacion via variables de entorno."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion global de la API, cargada desde variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "RIR-API"
    app_version: str = "1.0.0"

    # CORS
    cors_origins: list[str] = ["*"]

    # limites de archivos subidos
    max_upload_size_mb: int = 50

    # frecuencia de muestreo por defecto para generacion de senales
    default_fs: int = 48000


settings = Settings()
