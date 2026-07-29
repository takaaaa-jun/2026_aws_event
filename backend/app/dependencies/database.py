import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


def _load_env() -> None:
    app_dir = Path(__file__).resolve().parents[2]
    backend_dir = app_dir.parent
    project_dir = backend_dir.parent

    for env_path in (backend_dir / ".env", project_dir / ".env", Path("/app/.env")):
        if env_path.exists():
            load_dotenv(env_path, override=False)


def _database_url() -> str:
    _load_env()

    db_host = os.getenv("MYSQL_HOST", "db")
    if not Path("/.dockerenv").exists() and db_host in {"db", "mysql"}:
        db_host = "localhost"

    db_user = os.getenv("MYSQL_USER", "root")
    db_password = os.getenv("MYSQL_PASSWORD", "pass")
    db_port = os.getenv("MYSQL_PORT", "3306")
    db_database = os.getenv("MYSQL_DATABASE", "clinic")

    return (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_database}?charset=utf8mb4"
    )


engine = create_engine(_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
