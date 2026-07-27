from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from path_info import get_env_path


def create_env_data() -> dict:
    env_data = {}
    with open(get_env_path(), "r") as env:
        for line in env:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                env_data[key] = value
    return env_data


import os

def connection_database():
    env_data = create_env_data()

    # ローカル（Windows）から実行する場合、コンテナ名(dbやmysql)をlocalhostに自動で置き換えます
    # ただし、コンテナ内で実行されている場合は置き換えを行いません
    db_host = env_data["MYSQL_HOST"]
    if not os.path.exists('/.dockerenv') and db_host in ("db", "mysql"):
        db_host = "localhost"

    DATABASE = f"mysql+pymysql://{env_data['MYSQL_USER']}:{env_data['MYSQL_PASSWORD']}@{db_host}:{env_data['MYSQL_PORT']}/{env_data['MYSQL_DATABASE']}?charset=utf8mb4"

    engine = create_engine(DATABASE, echo=False)

    Base = declarative_base()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    session = scoped_session(session_factory)
    Base.query = session.query_property()

    return engine, session, Base
