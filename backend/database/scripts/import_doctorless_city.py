import os
import sys
import csv
from pathlib import Path

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from connection_database import connection_database
from models import DoctorlessCity, City
from path_info import get_doctorless_area_path
from log_decorator import Logger
from session import session
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

DOCTORLESS_CITY_CSV = get_doctorless_area_path() / "doctorless_city.csv"


def get_int_value(val):
    if not val or val.strip() == "":
        return None
    try:
        return int(float(val.strip().replace(",", "")))
    except ValueError:
        return None


def get_float_value(val):
    if not val or val.strip() == "":
        return None
    try:
        return float(val.strip())
    except ValueError:
        return None


def get_bool_value(val):
    if not val or val.strip() == "":
        return None
    val_clean = val.strip().lower()
    if val_clean in ("1", "true", "t", "y", "yes"):
        return True
    if val_clean in ("0", "false", "f", "n", "no"):
        return False
    return None


def import_csv_data():
    # 重複挿入を防ぐため、既存のデータをクリアします
    print("既存の無医地区（市区町村）データをクリアしています...")
    session.query(DoctorlessCity).delete()
    session.commit()

    if DOCTORLESS_CITY_CSV.exists():
        print(f"無医地区（市区町村）データのインポートを開始: {DOCTORLESS_CITY_CSV.name}")
        
        
        
        with open(DOCTORLESS_CITY_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                statement = (
                        select(City.city_id)
                        .where(City.city_raw_id == get_int_value(row.get("city_raw_id")) , City.city_name == row.get("city_name"))
                    )
                city_id = session.scalars(statement).first()
                doctorless_city = DoctorlessCity(
                    doctorless_city_id=city_id,
                    municipality_id=get_int_value(row.get("municipality_id")),
                    city_raw_id=get_int_value(row.get("city_raw_id")),
                    city_name=row.get("city_name"),
                    latitude=get_float_value(row.get("latitude")),
                    longitude=get_float_value(row.get("longitude")),
                    doctorless_flag=get_bool_value(row.get("doctorless_flag")),
                )
                session.add(doctorless_city)
        session.commit()
        print("すべてのデータのインポートが完了しました。")
    else:
        print(f"警告: CSVファイルが見つかりません: {DOCTORLESS_CITY_CSV}")


if __name__ == "__main__":
    logger = Logger()
    logger.start_point()
    try:
        import_csv_data()
        logger.end_point()
    except Exception as e:
        logger.error_point()
        logger.exception_point()
        raise e
