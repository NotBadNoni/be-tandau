import os
from pathlib import Path

from authlib.integrations.starlette_client import OAuth
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MEDIA_DIR = os.path.join(BASE_DIR / "media")
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    SECRET_KEY: str
    JWT_ACCESS_EXPIRE_MINUTES: int
    JWT_REFRESH_EXPIRE_MINUTES: int

    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    OPENAI_API_KEY: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = BASE_DIR / ".env"

    @property
    def async_db_url(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )

    @property
    def db_url(self):
        return "postgresql://{}:{}@{}:{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )


settings = Settings()
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    api_base_url="https://openidconnect.googleapis.com/v1/",
    client_kwargs={'scope': 'openid email profile'},
)
