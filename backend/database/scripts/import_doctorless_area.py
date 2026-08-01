import os
import sys
import csv
from pathlib import Path
from collections import defaultdict

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from connection_database import connection_database
from models import Prefecture, Municipality, City, AreaCity
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


def get_common_prefix(names):
    if not names:
        return ""
    names = [n.strip() for n in names if n]
    if not names:
        return ""
    
    shortest = min(names, key=len)
    for i, char in enumerate(shortest):
        for other in names:
            if i >= len(other) or other[i] != char:
                return shortest[:i]
    return shortest


def import_csv_data():
    # 重複挿入を防ぐため、既存の無医地区関連データをクリアします
    print("既存の無医地区データをクリアしています...")
    session.query(AreaCity).delete()
    session.query(City).delete()
    session.query(Municipality).delete()
    session.query(Prefecture).delete()
    session.commit()

    # 1. 都道府県データのインポート
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

    # 2. 市区町村データのインポート
    # prefecture_raw_id から DB上の prefecture_id を引くためのマップ
    prefectures = session.query(Prefecture).all()
    pref_map = {p.prefecture_raw_id: p.prefecture_id for p in prefectures}

    if MUNICIPALITIES_CSV.exists():
        print(f"市区町村データのインポートを開始: {MUNICIPALITIES_CSV.name}")
        with open(MUNICIPALITIES_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pref_raw_id = get_int_value(row.get("prefecture_raw_id"))
                pref_id = pref_map.get(pref_raw_id)
                if pref_id is None:
                    print(f"警告: 都道府県コード {pref_raw_id} がprefectureテーブルに見つかりません。スキップします。")
                    continue

                mun = Municipality(
                    municipality_id=get_int_value(row.get("municipality_id")),
                    prefecture_id=pref_id,
                    municipality_raw_id=get_int_value(row.get("municipality_raw_id")),
                    municipality_name=row.get("municipality_name"),
                )
                session.add(mun)
        session.commit()

    # 3. 地区・座標データのインポート (city と area_city)
    municipalities = session.query(Municipality).all()
    # (prefecture_raw_id, municipality_raw_id) から municipality_id を引くマップ
    # prefecture_raw_id は prefecture テーブルから持ってくる必要があります
    pref_raw_map = {p.prefecture_id: p.prefecture_raw_id for p in prefectures}
    mun_map = {}
    for m in municipalities:
        p_raw = pref_raw_map.get(m.prefecture_id)
        if p_raw is not None:
            mun_map[(p_raw, m.municipality_raw_id)] = m.municipality_id

    if AREA_CSV.exists():
        print(f"地区・座標データのインポートを開始: {AREA_CSV.name}")
        
        # データをメモリ上で (municipality_id, area_raw_id // 1000) でグループ化
        grouped_areas = defaultdict(list)
        with open(AREA_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pref_raw_id = get_int_value(row.get("prefecture_raw_id"))
                mun_raw_id = get_int_value(row.get("municipality_raw_id"))
                mun_id = mun_map.get((pref_raw_id, mun_raw_id))
                if mun_id is None:
                    continue

                area_raw_id = get_int_value(row.get("area_raw_id"))
                city_raw_id = area_raw_id // 1000

                key = (mun_id, city_raw_id)
                grouped_areas[key].append(row)

        print(f"集約グループ化完了。ユニークな町数: {len(grouped_areas)}")

        # 各グループの登録
        for key, row_list in grouped_areas.items():
            mun_id, city_raw_id = key

            # 共通部分を抽出して町名とする
            names = [r.get("area_name") for r in row_list]
            city_name = get_common_prefix(names)
            if not city_name:
                city_name = min(names, key=len).strip()

            # City（町マスタ）の登録
            city = City(
                municipality_id=mun_id,
                city_raw_id=city_raw_id,
                city_name=city_name
            )
            session.add(city)
            session.flush()  # city_id の発番

            # 座標データを AreaCity に登録
            for row in row_list:
                area_city = AreaCity(
                    city_id=city.city_id,
                    latitude=get_float_value(row.get("latitude")),
                    longitude=get_float_value(row.get("longitude"))
                )
                session.add(area_city)

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
