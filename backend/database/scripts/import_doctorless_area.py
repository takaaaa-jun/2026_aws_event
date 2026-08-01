import os
import sys
import csv
from pathlib import Path

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from connection_database import connection_database
from models import Prefecture, Municipality, Area
from path_info import get_doctorless_area_path
from log_decorator import Logger
from session import session

PREFECTURES_CSV = get_doctorless_area_path() / "prefectures.csv"
MUNICIPALITIES_CSV = get_doctorless_area_path() / "municipalities.csv"
AREA_CSV = get_doctorless_area_path() / "area.csv"


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


def import_csv_data():
    # 重複挿入を防ぐため、既存の無医地区関連データを削除して初期化します
    print("既存の無医地区データをクリアしています...")
    session.query(Area).delete()
    session.query(Municipality).delete()
    session.query(Prefecture).delete()
    session.commit()

    if PREFECTURES_CSV.exists():
        print(f"都道府県データのインポートを開始: {PREFECTURES_CSV.name}")
        with open(PREFECTURES_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pref = Prefecture(
                    prefecture_id=get_int_value(row.get("prefecture_id")),
                    prefecture_raw_id=get_int_value(row.get("prefecture_raw_id")),
                    prefecture_name=row.get("prefecture_name"),
                )
                session.add(pref)
        session.commit()

    if MUNICIPALITIES_CSV.exists():
        print(f"市区町村データのインポートを開始: {MUNICIPALITIES_CSV.name}")
        with open(MUNICIPALITIES_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mun = Municipality(
                    municipality_id=get_int_value(row.get("municipality_id")),
                    prefecture_raw_id=get_int_value(row.get("prefecture_raw_id")),
                    municipality_raw_id=get_int_value(row.get("municipality_raw_id")),
                    municipality_name=row.get("municipality_name"),
                )
                session.add(mun)
        session.commit()

    if AREA_CSV.exists():
        print(f"地区データのインポートを開始: {AREA_CSV.name}")
        with open(AREA_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                area = Area(
                    area_id=get_int_value(row.get("area_id")),
                    prefecture_raw_id=get_int_value(row.get("prefecture_raw_id")),
                    municipality_raw_id=get_int_value(row.get("municipality_raw_id")),
                    area_raw_id=get_int_value(row.get("area_raw_id")),
                    area_name=row.get("area_name"),
                    latitude=get_float_value(row.get("latitude")),
                    longitude=get_float_value(row.get("longitude")),
                    reference_id=get_int_value(row.get("reference_id")),
                    area_group=get_int_value(row.get("area_group")),
                )
                session.add(area)
        session.commit()

    print("すべてのデータのインポートが完了しました。")


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
