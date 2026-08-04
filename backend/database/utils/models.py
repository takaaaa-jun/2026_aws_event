from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

try:
    from .connection_database import connection_database
except ImportError:
    from connection_database import connection_database

_, _, Base = connection_database()


class Clinic(Base):
    __tablename__ = "clinic"

    clinic_id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_name = Column(String(255), nullable=True, index=True)
    clinic_postcode = Column(Text, nullable=True)
    clinic_address = Column(Text, nullable=True)
    clinic_tel = Column(Text, nullable=True)
    opening_date = Column(Text, nullable=True)
    establisher = Column(Text, nullable=True)
    general_bed = Column(Integer, nullable=True)
    recuperation_bed = Column(Integer, nullable=True)
    remarks = Column(Text, nullable=True)
    signpost_flag = Column(Boolean, nullable=True)

    latitude_longitude = relationship(
        "LatitudeLongitude", back_populates="clinic", uselist=False
    )
    departments = relationship("ClinicDepartment", back_populates="clinic")


class LatitudeLongitude(Base):
    __tablename__ = "latitude_longitude"

    ll_id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False, index=True)
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)

    clinic = relationship("Clinic", back_populates="latitude_longitude")



class Department(Base):
    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(Text, nullable=True)

    clinics = relationship("ClinicDepartment", back_populates="department")


class ClinicDepartment(Base):
    __tablename__ = "clinic_department"

    clinic_department_id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False, index=True)
    department_id = Column(
        Integer, ForeignKey("department.department_id"), nullable=False, index=True
    )

    clinic = relationship("Clinic", back_populates="departments")
    department = relationship("Department", back_populates="clinics")


class Prefecture(Base):
    __tablename__ = "prefecture"

    prefecture_id = Column(Integer, primary_key=True, autoincrement=True)
    prefecture_raw_id = Column(Integer, nullable=False, index=True)
    prefecture_name = Column(String(255), nullable=True, index=True)


class Municipality(Base):
    __tablename__ = "municipality"

    municipality_id = Column(Integer, primary_key=True, autoincrement=True)
    prefecture_id = Column(Integer, ForeignKey("prefecture.prefecture_id"), nullable=False, index=True)
    municipality_raw_id = Column(Integer, nullable=False, index=True)
    municipality_name = Column(String(255), nullable=True, index=True)


class City(Base):
    __tablename__ = "city"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    municipality_id = Column(Integer, ForeignKey("municipality.municipality_id"), nullable=False, index=True)
    city_raw_id = Column(Integer, nullable=False, index=True)
    city_name = Column(String(255), nullable=True, index=True)

    areas = relationship("AreaCity", back_populates="city")


class AreaCity(Base):
    __tablename__ = "area_city"

    area_city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("city.city_id"), nullable=False, index=True)
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)
    doctorless_flag = Column(Boolean, nullable=True)

    city = relationship("City", back_populates="areas")


class DoctorlessCity(Base):
    __tablename__ = "doctorless_city"

    # city_id の値が入るが、cityテーブルへのForeignKey制約は持たせない
    # 手動でIDを挿入するため、autoincrement=False を設定する
    doctorless_city_id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    municipality_id = Column(Integer, ForeignKey("municipality.municipality_id"), nullable=False, index=True)
    city_raw_id = Column(Integer, nullable=False, index=True)
    city_name = Column(String(255), nullable=True, index=True)
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)
    doctorless_flag = Column(Boolean, nullable=True)

    municipality = relationship("Municipality")


class DoctorlessCityInternal(Base):
    __tablename__ = "doctorless_city_internal"

    # doctorless_city と全く同じ構造
    doctorless_city_id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    municipality_id = Column(Integer, ForeignKey("municipality.municipality_id"), nullable=False, index=True)
    city_raw_id = Column(Integer, nullable=False, index=True)
    city_name = Column(String(255), nullable=True, index=True)
    latitude = Column(Double, nullable=True)
    longitude = Column(Double, nullable=True)
    doctorless_flag = Column(Boolean, nullable=True)

    municipality = relationship("Municipality")



