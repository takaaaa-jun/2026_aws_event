import os
import sys
import csv
from pathlib import Path
from collections import defaultdict

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from models import Prefecture, Municipality, City, AreaCity
from path_info import get_doctorless_area_path
from session import session

ORIGINAL_CSV = get_doctorless_area_path() / "_15_2025.csv"


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


def verify_data():
    if not ORIGINAL_CSV.exists():
        print(f"エラー: 元データファイルが見つかりません: {ORIGINAL_CSV}")
        sys.exit(1)

    print("データベースからインポートされたデータを取得中...")
    prefectures = session.query(Prefecture).all()
    municipalities = session.query(Municipality).all()
    cities = session.query(City).all()
    area_cities = session.query(AreaCity).all()

    # マッピングの作成
    pref_map = {p.prefecture_raw_id: p for p in prefectures}
    mun_map = {(m.prefecture_id, m.municipality_raw_id): m for m in municipalities}
    city_map = {(c.municipality_id, c.city_raw_id): c for c in cities}

    # 各city_idに紐づく座標リスト
    coords_by_city = defaultdict(list)
    for ac in area_cities:
        coords_by_city[ac.city_id].append((ac.latitude, ac.longitude))

    # 市区町村IDから都道府県IDを引くマップ
    mun_pref_map = {m.municipality_id: m.prefecture_id for m in municipalities}
    pref_id_to_raw = {p.prefecture_id: p.prefecture_raw_id for p in prefectures}

    print(f"DB登録数 - 都道府県: {len(prefectures)}, 市区町村: {len(municipalities)}, 町: {len(cities)}, 座標点: {len(area_cities)}")

    total_rows = 0
    mismatches = 0
    missing_prefecture = 0
    missing_municipality = 0
    missing_city = 0
    missing_coord = 0

    print("元データ (CSV) との照合を開始します...")
    with open(ORIGINAL_CSV, mode="r", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1

            pref_raw_id = get_int_value(row.get("都道府県コード"))
            mun_code = get_int_value(row.get("市区町村コード"))
            area_code_str = row.get("大字町丁目コード", "").strip()

            # IDのパース
            mun_raw_id = mun_code % 1000 if mun_code is not None else None
            city_raw_id = (int(area_code_str[5:]) // 1000) if area_code_str and len(area_code_str) >= 12 else None


            # 1. 都道府県のチェック
            pref = pref_map.get(pref_raw_id)
            if not pref:
                missing_prefecture += 1
                mismatches += 1
                print(f"不一致 [都道府県未登録]: コード {pref_raw_id}")
                continue
            
            if pref.prefecture_name != row.get("都道府県名"):
                mismatches += 1
                print(f"不一致 [都道府県名]: DB '{pref.prefecture_name}' vs CSV '{row.get('都道府県名')}'")

            # 2. 市区町村のチェック
            mun = mun_map.get((pref.prefecture_id, mun_raw_id))
            if not mun:
                missing_municipality += 1
                mismatches += 1
                print(f"不一致 [市区町村未登録]: 都道府県 {pref_raw_id}, 市区町村コード {mun_code} (JIS: {mun_raw_id})")
                continue

            if mun.municipality_name != row.get("市区町村名"):
                mismatches += 1
                print(f"不一致 [市区町村名]: DB '{mun.municipality_name}' vs CSV '{row.get('市区町村名')}'")

            # 3. 町のチェック
            city = city_map.get((mun.municipality_id, city_raw_id))
            if not city:
                missing_city += 1
                mismatches += 1
                print(f"不一致 [町未登録]: 市区町村 {mun.municipality_name}, 町コード {city_raw_id}")
                continue

            # 地名の前方一致チェック
            csv_area_name = row.get("大字町丁目名", "").strip()
            db_city_name = city.city_name or ""
            if not csv_area_name.startswith(db_city_name):
                mismatches += 1
                print(f"不一致 [町名 (前方一致不適合)]: DB '{db_city_name}' vs CSV '{csv_area_name}'")

            # 4. 座標のチェック (誤差1e-7以内で一致する座標が同一city_id内に存在するか)
            csv_lat = get_float_value(row.get("緯度"))
            csv_lng = get_float_value(row.get("経度"))
            
            coord_matched = False
            if csv_lat is not None and csv_lng is not None:
                for db_lat, db_lng in coords_by_city.get(city.city_id, []):
                    if db_lat is not None and db_lng is not None:
                        if abs(db_lat - csv_lat) < 1e-7 and abs(db_lng - csv_lng) < 1e-7:
                            coord_matched = True
                            break

            if not coord_matched:
                missing_coord += 1
                mismatches += 1
                print(f"不一致 [座標不一致 / 未登録]: 町 {db_city_name} (ID {city.city_id}), CSV座標 ({csv_lat}, {csv_lng})")

    print("\n--- 照合結果 ---")
    print(f"CSV総行数: {total_rows}")
    print(f"不一致レコード数: {mismatches}")
    print(f"未登録の都道府県: {missing_prefecture}")
    print(f"未登録の市区町村: {missing_municipality}")
    print(f"未登録の町: {missing_city}")
    print(f"未登録・不一致の座標点: {missing_coord}")

    if mismatches == 0:
        print("検証成功")
    else:
        print("検証失敗")


if __name__ == "__main__":
    verify_data()
