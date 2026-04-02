from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from app.infrastructure.database.config import settings

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create .env file with DATABASE_URL=postgresql://..."
    )

engine = create_engine(
    settings.database_url,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    pool_pre_ping=settings.pool_pre_ping,
    pool_recycle=settings.pool_recycle,
    echo=settings.echo,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """Dependency для FastAPI. Создает сессию на каждый request."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()