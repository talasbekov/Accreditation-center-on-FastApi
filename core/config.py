from pydantic import BaseSettings, Extra
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    API_V1_PREFIX: str

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    templates = Jinja2Templates(directory="./templates")

    AUTHJWT_SECRET_KEY: str
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    authjwt_cookie_csrf_protect: bool = False  # отключите, если CSRF не используется
    authjwt_cookie_samesite: str = "lax"  # для работы с кросс-доменными запросами
    authjwt_cookie_secure: bool = False  # установите в True для HTTPS

    DEBUG: bool = True
    SENTRY_DSN: str = None

    GENERATE_IP: str = None
    SQLALCHEMY_ECHO: bool = False

    SENTRY_ENABLED: bool = False


    SERVICE_PASSWORD: str

    class Config:
        extra = Extra.allow
        env_file = ".env"


configs = Settings()
