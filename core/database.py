import logging

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import configs

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=configs.SQLALCHEMY_ECHO
)

# Создаем фабрику асинхронных сессий с использованием async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)

Base = declarative_base()

# Асинхронная функция получения сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            logging.error(f"Произошла ошибка при работе с базой данных: {e}")
            raise
        finally:
            await db.close()
            logging.debug("Database connection closed.")
