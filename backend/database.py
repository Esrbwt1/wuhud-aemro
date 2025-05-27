from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# DATABASE_URL for SQLite. This will create a file named wuhudaemro.db in the backend directory.
# We use os.getenv for potential future flexibility (e.g., moving to PostgreSQL on Render)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wuhudaemro.db")

# create_engine is the starting point for any SQLAlchemy application.
# connect_args is needed only for SQLite to allow multithreaded access.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Needed only for SQLite
)

# Each instance of the SessionLocal class will be a database session.
# The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base will be used by our ORM models to inherit from.
Base = declarative_base()

# Dependency to get DB session for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()