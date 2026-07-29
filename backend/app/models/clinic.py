from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.dependencies.database import Base


class Clinic(Base):
    __tablename__ = "clinic"

    clinic_id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_name = Column(String(255), nullable=True)
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
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    clinic = relationship("Clinic", back_populates="latitude_longitude")


class Department(Base):
    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(Text, nullable=True)

    clinics = relationship("ClinicDepartment", back_populates="department")


class ClinicDepartment(Base):
    __tablename__ = "clinic_department"

    clinic_department_id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_id = Column(Integer, ForeignKey("clinic.clinic_id"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.department_id"), nullable=False)

    clinic = relationship("Clinic", back_populates="departments")
    department = relationship("Department", back_populates="clinics")
