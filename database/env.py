
import os, sys

from logging.config import fileConfig
from typing import List

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool

from alembic import context

load_dotenv()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    db_connection = os.getenv("DB_CONNECTION", "postgresql")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "")
    db_database = os.getenv("DB_DATABASE", "app")
    return f"{db_connection}://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"

def _include_object(target_schema):
    def include_object(obj, name, object_type, reflected, compare_to):
        if object_type == "table":
            return obj.schema in target_schema
        else:
            return True

    return include_object


def run_migrations_offline(target_metadata, schema):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,  #1
        include_object=_include_object(schema),  #1
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(target_metadata, schema):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_schemas=True,  #2
            include_object=_include_object(schema),  #2
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations(metadata: MetaData, schema: List[str]):
    if context.is_offline_mode():
        run_migrations_offline(metadata, schema)
    else:
        run_migrations_online(metadata, schema)
