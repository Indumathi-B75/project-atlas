
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project root: ~/project-atlas
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load the project's .env file automatically.
# Existing environment variables take precedence.
load_dotenv(PROJECT_ROOT / ".env", override=False)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Check that the project-root .env "
        "file exists and contains DATABASE_URL."
    )

# Create the SQLAlchemy database engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create individual database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    """Provide a database session and close it after use."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
