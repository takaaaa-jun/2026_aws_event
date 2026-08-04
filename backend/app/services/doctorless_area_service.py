from sqlalchemy.orm import Session

from app.repositories.doctorless_area_repository import DoctorlessAreaRepository
from app.schemas.doctorless_area import (
    DoctorlessAreaListMetaResponse,
    DoctorlessAreaLocationResponse,
    DoctorlessAreaResponse,
    DoctorlessAreasResponse,
)


class DoctorlessAreaService:
    def __init__(
        self, doctorless_area_repository: DoctorlessAreaRepository | None = None
    ) -> None:
        self.doctorless_area_repository = (
            doctorless_area_repository or DoctorlessAreaRepository()
        )

    def list_doctorless_areas(
        self, db: Session, limit: int
    ) -> DoctorlessAreasResponse:
        doctorless_areas = self.doctorless_area_repository.list_doctorless_areas(
            db=db, limit=limit
        )

        return DoctorlessAreasResponse(
            meta=DoctorlessAreaListMetaResponse(
                limit=limit, count=len(doctorless_areas)
            ),
            data=[
                DoctorlessAreaResponse(
                    doctorless_city_id=doctorless_area.doctorless_city_id,
                    municipality_id=doctorless_area.municipality_id,
                    municipality_name=(
                        doctorless_area.municipality.municipality_name
                        if doctorless_area.municipality
                        else None
                    ),
                    city_raw_id=doctorless_area.city_raw_id,
                    city_name=doctorless_area.city_name,
                    doctorless_flag=doctorless_area.doctorless_flag,
                    location=DoctorlessAreaLocationResponse(
                        latitude=doctorless_area.latitude,
                        longitude=doctorless_area.longitude,
                    ),
                )
                for doctorless_area in doctorless_areas
            ],
        )
