import os
import time
from typing import Generator
from sqlalchemy import text
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

# Load environment variables from .env file (if not running in Docker, Docker handles it)
load_dotenv()

# Retrieve DB Credentials from Environment
# The environment variables are passed from the docker-compose.yml
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Create the MySQL connection URL
# Note: This is crucial. It uses the service name 'db' as the hostname.
SQLALCHEMY_DATABASE_URL = (
    # f"mysql+mysqlclient://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False, # Set to True for development debugging
    pool_recycle=3600
)


# Dependency function to get the SQLModel session
def get_session() -> Generator[Session, None, None]:
    """Provides a transactional database session using SQLModel."""
    # Session is a context manager, preferred by SQLModel
    with Session(engine) as session:
        yield session


# Alembic will use SQLModel.metadata to discover all classes that inherit from SQLModel
metadata = SQLModel.metadata

def wait_for_db():
    """Wait for the database to accept connections."""
    max_retries = 10
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return
        except OperationalError:
            print(f"Database not ready yet (attempt {i+1})")
            time.sleep(3)
    raise Exception("Could not connect to database")
