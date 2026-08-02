from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.clinic import ClinicsResponse
from app.services.clinic_service import ClinicService

router = APIRouter(prefix="/api/v1/clinics", tags=["clinics"])
clinic_service = ClinicService()

# APIエンドポイント
@router.get("", response_model=ClinicsResponse)
def list_clinics(limit: int, db: Session = Depends(get_db)) -> ClinicsResponse:
    return clinic_service.list_clinics(db=db, limit=limit)
