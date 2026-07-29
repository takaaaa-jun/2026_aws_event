from sqlalchemy.orm import Session

from app.repositories.clinic_repository import ClinicRepository
from app.schemas.clinic import (
    ClinicListMetaResponse,
    ClinicLocationResponse,
    ClinicResponse,
    ClinicsResponse,
    DepartmentResponse,
)


class ClinicService:
    def __init__(self, clinic_repository: ClinicRepository | None = None) -> None:
        self.clinic_repository = clinic_repository or ClinicRepository()

    def list_clinics(self, db: Session, limit: int) -> ClinicsResponse:
        clinics = self.clinic_repository.list_clinics(db=db, limit=limit)
        departments = self.clinic_repository.list_departments(db=db)

        return ClinicsResponse(
            meta=ClinicListMetaResponse(limit=limit, count=len(clinics)),
            departments=[
                DepartmentResponse(
                    department_id=department.department_id,
                    department_name=department.department_name,
                )
                for department in departments
            ],
            data=[
                ClinicResponse(
                    clinic_id=clinic.clinic_id,
                    clinic_name=clinic.clinic_name,
                    clinic_postcode=clinic.clinic_postcode,
                    clinic_address=clinic.clinic_address,
                    clinic_tel=clinic.clinic_tel,
                    opening_date=clinic.opening_date,
                    establisher=clinic.establisher,
                    general_bed=clinic.general_bed,
                    recuperation_bed=clinic.recuperation_bed,
                    remarks=clinic.remarks,
                    signpost_flag=clinic.signpost_flag,
                    location=ClinicLocationResponse(
                        latitude=(
                            clinic.latitude_longitude.latitude
                            if clinic.latitude_longitude
                            else None
                        ),
                        longitude=(
                            clinic.latitude_longitude.longitude
                            if clinic.latitude_longitude
                            else None
                        ),
                    ),
                    departments=[
                        DepartmentResponse(
                            department_id=clinic_department.department.department_id,
                            department_name=clinic_department.department.department_name,
                        )
                        for clinic_department in clinic.departments
                        if clinic_department.department is not None
                    ],
                )
                for clinic in clinics
            ],
        )
