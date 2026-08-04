from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.doctorless_area import DoctorlessAreasResponse
from app.services.doctorless_area_service import DoctorlessAreaService

router = APIRouter(prefix="/api/v1/doctorless_area", tags=["doctorless_area"])
doctorless_area_service = DoctorlessAreaService()


@router.get("", response_model=DoctorlessAreasResponse)
def list_doctorless_areas(
    limit: int, db: Session = Depends(get_db)
) -> DoctorlessAreasResponse:
    return doctorless_area_service.list_doctorless_areas(db=db, limit=limit)
