# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.database import Base  # Указываем полный путь
from app.schemas import *
import os

# Загрузим конфигурацию Alembic
config = context.config

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST_PORT = os.getenv("POSTGRES_HOST_PORT", "localhost:5432")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_PORT}/{POSTGRES_DB}"

if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise ValueError("DATABASE_URL environment variable is not set")

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем модель базы данных для автоматических миграций
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine,
    though an Engine is also acceptable here. By skipping the Engine creation
    we don't need a database connection. Calls to context.execute()
    here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
