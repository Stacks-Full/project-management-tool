from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from dotenv import load_dotenv

from sqlmodel import SQLModel
from app.core.models import *

load_dotenv()

sys.path.append(os.path.abspath("."))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata


def process_revision_directives(context, revision, directives) -> None:
    """Drop empty auto-generated migrations to avoid noise."""
    if not directives:
        return
    directive = directives[0]
    # ScriptDirectory / MigrationScript has .upgrade_ops for autogen
    upgrade_ops = getattr(directive, "upgrade_ops", None)
    if upgrade_ops and not upgrade_ops.ops:
        # Remove directive to skip creating an empty migration file
        directives[:] = []


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_db_url():
    """Constructs the database URL from environment variables."""
    db_dialect = os.getenv("DB_DIALECT", "mysql+mysqldb")

    db_user = os.getenv("DB_USER", "root")
    # Removed the default value, requiring it to be set by the environment
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")

    default_port = "3306" if "mysql" in db_dialect else "5432"
    db_port = os.getenv("DB_PORT", default_port)

    db_name = os.getenv("DB_NAME", "generic_db")

    # DB_PASSWORD is now included in this list
    required_vars = {"DB_USER": db_user, "DB_PASSWORD": db_pass, "DB_NAME": db_name}

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        print(
            f"Error: Missing required environment variables for database connection: {', '.join(missing_vars)}"
        )
        # This will raise excpetion fail fast
        raise Exception(
            "Database configuration incomplete. Please set required DB environment variables."
        )

    # Use the dialect variable in the f-string
    return f"{db_dialect}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url") or get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=False,
        compare_type=True,
        compare_server_default=True,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_url = get_db_url()
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=db_url,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=False,
            compare_type=True,
            compare_server_default=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
