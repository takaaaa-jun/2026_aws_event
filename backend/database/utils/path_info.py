from pathlib import Path

import os

CURRENT_FILE_PATH = Path(__file__).resolve()
ROOT_DIR_PATH = CURRENT_FILE_PATH.parent.parent.parent

if os.path.exists('/.dockerenv'):
    ENV_FILE_PATH = ROOT_DIR_PATH / ".env"
else:
    ENV_FILE_PATH = ROOT_DIR_PATH.parent / ".env"

SQL_DIR_PATH = ROOT_DIR_PATH / "data" / "sql"
GEOCODING_DIR_PATH = ROOT_DIR_PATH / "data" / "geocoding"
DOCTORLESS_AREA_DIR_PATH = ROOT_DIR_PATH / "data" / "doctorless_area"

def get_env_path() -> Path:
    return ENV_FILE_PATH

def get_sql_path() -> Path:
    return SQL_DIR_PATH

def get_geocoding_path() -> Path:
    return GEOCODING_DIR_PATH

def get_doctorless_area_path() -> Path:
    return DOCTORLESS_AREA_DIR_PATH