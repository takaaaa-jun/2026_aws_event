import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

try:
    from .connection_database import create_env_data
except ImportError:
    from connection_database import create_env_data

env_data = create_env_data()

db_host = env_data.get("MYSQL_HOST", "db")
if not os.path.exists('/.dockerenv') and db_host in ("db", "mysql"):
    db_host = "localhost"

db_user = env_data.get("MYSQL_USER", "root")
db_password = env_data.get("MYSQL_PASSWORD", "pass")
db_port = env_data.get("MYSQL_PORT", "3306")
db_database = env_data.get("MYSQL_DATABASE", "clinic")

DATABASE = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?charset=utf8mb4"

engine = create_engine(DATABASE)


Base = declarative_base()
session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
session = scoped_session(session_factory)
Base.query = session.query_property()
