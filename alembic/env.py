from logging.config import fileConfig
import asyncio
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from core import configs
from core import Base  # Убедитесь, что этот импорт корректно ссылается на вашу базу моделей

# Объект конфигурации Alembic
config = context.config

# Установка URL для SQLAlchemy с использованием драйвера asyncpg
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+asyncpg://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_HOSTNAME}:{configs.DATABASE_PORT}/{configs.POSTGRES_DB}",
)

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для поддержки автогенерации
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запустить миграции в 'offline' режиме."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Запустить миграции в 'online' режиме с использованием асинхронного движка."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
