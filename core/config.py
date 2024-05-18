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

    AUTHJWT_SECRET_KEY: str
    AUTHJWT_TOKEN_LOCATION: set = {"cookies"}
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    authjwt_cookie_csrf_protect: bool = False

    DEBUG: bool = False
    SENTRY_DSN: str = None

    GENERATE_IP: str = None
    SQLALCHEMY_ECHO: bool = False

    SENTRY_ENABLED: bool = False

    templates = Jinja2Templates(directory="./templates")
    authjwt_token_location: set = {"cookies"}

    class Config:
        extra = Extra.allow
        env_file = ".env"


configs = Settings()
