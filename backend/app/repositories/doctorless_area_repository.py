from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database.utils.models import DoctorlessCity


class DoctorlessAreaRepository:
    def list_doctorless_areas(
        self, db: Session, limit: int
    ) -> list[DoctorlessCity]:
        if limit <= 0:
            return []

        statement = (
            select(DoctorlessCity)
            .options(selectinload(DoctorlessCity.municipality))
            .where(DoctorlessCity.doctorless_flag.is_(True))
            .order_by(DoctorlessCity.doctorless_city_id)
            .limit(limit)
        )
        return list(db.scalars(statement).all())
