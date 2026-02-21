from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

engine_kwargs = {"echo": False}  # set True to log SQL statements during development
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite-specific option: allows multi-thread access in local dev.
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)


def create_db_and_tables() -> None:
    """Create all tables defined in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency that yields a database session."""
    with Session(engine) as session:
        yield session
