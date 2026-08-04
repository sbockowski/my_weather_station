from collections.abc import Iterator
from sqlmodel import create_engine, Session, SQLModel

sqlite_url = "sqlite:///weather.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables() -> None:
    """Tworzy plik bazy oraz tabele na podstawie modeli SQLModel."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Generator sesji bazy danych używany jako Dependency w FastAPI."""
    with Session(engine) as session:
        yield session
