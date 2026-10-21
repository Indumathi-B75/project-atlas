
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read the database URL supplied by the environment.
DATABASE_URL = os.environ["DATABASE_URL"]

# Engine: manages connections between Python and PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# SessionLocal: creates individual database sessions.
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
