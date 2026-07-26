from pathlib import Path

CURRENT_FILE_PATH = Path(__file__).resolve()
ROOT_DIR_PATH = CURRENT_FILE_PATH.parent.parent.parent
ENV_FILE_PATH = ROOT_DIR_PATH / ".env"
SQL_DIR_PATH = ROOT_DIR_PATH / "data" / "sql"

def get_env_path() -> Path:
    return ENV_FILE_PATH

def get_sql_path() -> Path:
    return SQL_DIR_PATH