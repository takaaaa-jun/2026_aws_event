from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database.utils.models import Clinic, ClinicDepartment, Department


class ClinicRepository:
    def list_clinics(self, db: Session, limit: int) -> list[Clinic]:
        if limit <= 0:
            return []

        statement = (
            select(Clinic)
            .options(
                selectinload(Clinic.latitude_longitude),
                selectinload(Clinic.departments).selectinload(
                    ClinicDepartment.department
                ),
            )
            .order_by(Clinic.clinic_id)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def list_departments(self, db: Session) -> list[Department]:
        statement = select(Department).order_by(Department.department_id)
        return list(db.scalars(statement).all())
