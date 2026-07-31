from typing import Generator
from sqlalchemy.orm import Session
from database.utils.connection_database import connection_database

engine, SessionLocal, _ = connection_database()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        SessionLocal.remove()
