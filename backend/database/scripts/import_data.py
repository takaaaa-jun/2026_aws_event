import os
import sys
import csv
from pathlib import Path

utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from connection_database import connection_database
from models import Clinic, LatitudeLongitude, Department, ClinicDepartment
from path_info import get_geocoding_path
from log_decorator import Logger

CLINICS_CSV = get_geocoding_path() / "R8_Niigata_Clinics_All.csv"
DENTAL_CSV = get_geocoding_path() / "R8_Niigata_DentalClinics_All.csv"


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
    _, session, _ = connection_database()

    general_dept_names = [
        "内科",
        "呼吸器内科",
        "循環器内科",
        "消化器内科",
        "腎臓内科",
        "神経内科",
        "糖尿病内科",
        "血液内科",
        "皮膚科",
        "アレルギー科",
        "リウマチ科",
        "感染症内科",
        "小児科",
        "精神科",
        "心療内科",
        "外科",
        "呼吸器外科",
        "循環器外科",
        "乳腺外科",
        "気管食道外科",
        "消化器外科",
        "泌尿器科",
        "肛門外科",
        "脳神経外科",
        "整形外科",
        "形成外科",
        "美容外科",
        "眼科",
        "耳鼻咽喉科",
        "小児外科",
        "産婦人科",
        "産科",
        "婦人科",
        "リハビリテーション科",
        "放射線科",
        "麻酔科",
        "病理診断科",
        "臨床検査科",
        "救急科",
    ]
    dental_dept_names = ["歯科", "矯正", "小歯", "口腔"]

    all_departments = list(set(general_dept_names + dental_dept_names))

    dept_map = {}
    for name in all_departments:
        dept = session.query(Department).filter_by(department_name=name).first()
        if not dept:
            dept = Department(department_name=name)
            session.add(dept)
            session.flush()
        dept_map[name] = dept.department_id

    if CLINICS_CSV.exists():
        print(f"一般クリニックデータのインポートを開始: {CLINICS_CSV.name}")
        with open(CLINICS_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clinic = Clinic(
                    clinic_name=row.get("施設名"),
                    clinic_postcode=row.get("〒"),
                    clinic_address=f"{row.get('所在地1', '')}{row.get('所在地2', '')}",
                    clinic_tel=row.get("℡"),
                    opening_date=row.get("開　 設 年月日"),
                    establisher=row.get("解説者"),
                    general_bed=get_int_value(row.get("一般病床")),
                    recuperation_bed=get_int_value(row.get("療養病床")),
                    remarks=row.get("備考"),
                    signpost_flag=None,
                )
                session.add(clinic)
                session.flush()

                lat = get_float_value(row.get("緯度"))
                lng = get_float_value(row.get("経度"))
                if lat is not None or lng is not None:
                    ll = LatitudeLongitude(
                        clinic_id=clinic.clinic_id, latitude=lat, longitude=lng
                    )
                    session.add(ll)

                for dept_name in general_dept_names:
                    if row.get(dept_name) == "1":
                        cd = ClinicDepartment(
                            clinic_id=clinic.clinic_id,
                            department_id=dept_map[dept_name],
                        )
                        session.add(cd)

    if DENTAL_CSV.exists():
        print(f"歯科クリニックデータのインポートを開始: {DENTAL_CSV.name}")
        with open(DENTAL_CSV, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clinic = Clinic(
                    clinic_name=row.get("施設名"),
                    clinic_postcode=row.get("〒"),
                    clinic_address=f"{row.get('所在地1', '')}{row.get('所在地2', '')}",
                    clinic_tel=row.get("℡"),
                    opening_date=row.get("開　 設 年月日"),
                    establisher=row.get("開設者"),
                    general_bed=None,
                    recuperation_bed=None,
                    remarks=row.get("備考"),
                    signpost_flag=None,
                )
                session.add(clinic)
                session.flush()

                lat = get_float_value(row.get("緯度"))
                lng = get_float_value(row.get("経度"))
                if lat is not None or lng is not None:
                    ll = LatitudeLongitude(
                        clinic_id=clinic.clinic_id, latitude=lat, longitude=lng
                    )
                    session.add(ll)

                for dept_name in dental_dept_names:
                    if row.get(dept_name) == "1":
                        cd = ClinicDepartment(
                            clinic_id=clinic.clinic_id,
                            department_id=dept_map[dept_name],
                        )
                        session.add(cd)

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
