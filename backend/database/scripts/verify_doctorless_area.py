import os
import sys
import csv
from pathlib import Path

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from models import Prefecture, Municipality, Area
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
    areas = session.query(Area).all()

    pref_map = {p.prefecture_raw_id: p for p in prefectures}
    mun_map = {(m.prefecture_raw_id, m.municipality_raw_id): m for m in municipalities}
    area_map = {(a.prefecture_raw_id, a.municipality_raw_id, a.area_raw_id): a for a in areas}

    print(f"DB登録数 - 都道府県: {len(prefectures)}, 市区町村: {len(municipalities)}, 地区: {len(areas)}")

    total_rows = 0
    mismatches = 0
    missing_prefecture = 0
    missing_municipality = 0
    missing_area = 0

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
            area_raw_id = int(area_code_str[5:]) if area_code_str and len(area_code_str) >= 12 else None

            # 都道府県のチェック
            pref = pref_map.get(pref_raw_id)
            if not pref:
                missing_prefecture += 1
                mismatches += 1
                print(f"不一致 [都道府県未登録]: コード {pref_raw_id}")
                continue
            
            if pref.prefecture_name != row.get("都道府県名"):
                mismatches += 1
                print(f"不一致 [都道府県名]: DB '{pref.prefecture_name}' vs CSV '{row.get('都道府県名')}'")

            # 市区町村のチェック
            mun = mun_map.get((pref_raw_id, mun_raw_id))
            if not mun:
                missing_municipality += 1
                mismatches += 1
                print(f"不一致 [市区町村未登録]: 都道府県 {pref_raw_id}, 市区町村コード {mun_code} (JIS: {mun_raw_id})")
                continue

            if mun.municipality_name != row.get("市区町村名"):
                mismatches += 1
                print(f"不一致 [市区町村名]: DB '{mun.municipality_name}' vs CSV '{row.get('市区町村名')}'")

            # 地区のチェック
            area = area_map.get((pref_raw_id, mun_raw_id, area_raw_id))
            if not area:
                missing_area += 1
                mismatches += 1
                print(f"不一致 [地区未登録]: 都道府県 {pref_raw_id}, 市区町村 {mun_raw_id}, 地区コード {area_raw_id}")
                continue

            # 詳細データのチェック
            errors = []
            if area.area_name != row.get("大字町丁目名"):
                errors.append(f"地区名: DB '{area.area_name}' vs CSV '{row.get('大字町丁目名')}'")

            csv_lat = get_float_value(row.get("緯度"))
            csv_lng = get_float_value(row.get("経度"))
            if csv_lat is not None and (area.latitude is None or abs(area.latitude - csv_lat) > 1e-7):
                errors.append(f"緯度: DB {area.latitude} vs CSV {csv_lat}")
            if csv_lng is not None and (area.longitude is None or abs(area.longitude - csv_lng) > 1e-7):
                errors.append(f"経度: DB {area.longitude} vs CSV {csv_lng}")

            csv_ref_id = get_int_value(row.get("原典資料コード"))
            if area.reference_id != csv_ref_id:
                errors.append(f"原典資料コード: DB {area.reference_id} vs CSV {csv_ref_id}")

            csv_area_group = get_int_value(row.get("大字・字・丁目区分コード"))
            if area.area_group != csv_area_group:
                errors.append(f"区分コード: DB {area.area_group} vs CSV {csv_area_group}")

            if errors:
                mismatches += 1
                print(f"データ不一致 [地区ID {area.area_id}]: {', '.join(errors)}")

    print("\n--- 照合結果 ---")
    print(f"CSV総行数: {total_rows}")
    print(f"不一致レコード数: {mismatches}")
    print(f"未登録の都道府県: {missing_prefecture}")
    print(f"未登録の市区町村: {missing_municipality}")
    print(f"未登録の地区: {missing_area}")

    if mismatches == 0:
        print("検証成功")
    else:
        print("検証失敗")


if __name__ == "__main__":
    verify_data()
