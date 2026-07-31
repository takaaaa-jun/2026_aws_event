from pydantic import BaseModel


class ClinicLocationResponse(BaseModel):
    latitude: float | None
    longitude: float | None


class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str | None


class ClinicResponse(BaseModel):
    clinic_id: int
    clinic_name: str | None
    clinic_postcode: str | None
    clinic_address: str | None
    clinic_tel: str | None
    opening_date: str | None
    establisher: str | None
    general_bed: int | None
    recuperation_bed: int | None
    remarks: str | None
    signpost_flag: bool | None
    location: ClinicLocationResponse
    departments: list[DepartmentResponse]


class ClinicListMetaResponse(BaseModel):
    limit: int
    count: int


class ClinicsResponse(BaseModel):
    meta: ClinicListMetaResponse
    departments: list[DepartmentResponse]
    data: list[ClinicResponse]
