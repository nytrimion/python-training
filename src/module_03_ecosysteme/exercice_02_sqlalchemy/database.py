"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connection string for Docker PostgreSQL
DATABASE_URL = "postgresql://training:training@localhost:5432/training"

# Engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries
    pool_pre_ping=True,  # Verify connections before using
)

# Session factory
SessionLocal = sessionmaker(bind=engine)
