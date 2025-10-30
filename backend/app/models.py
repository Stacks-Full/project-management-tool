from sqlalchemy import Column, Integer, String
from .database import Base, engine

class Project(Base):
    """
    A minimal SQLAlchemy model representing a 'Project' in the database.
    This helps us test the database connection and ORM setup.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))

# Create tables in the database (if they don't exist)
# NOTE: In a real app, Alembic is used for migrations, but this is fine for dev setup.
def create_db_tables():
    """Attempts to create all defined tables in the connected database."""
    print("Attempting to create database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully or already exist.")
    except Exception as e:
        print(f"Error creating tables: {e}")
