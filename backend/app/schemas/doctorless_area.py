from pydantic import BaseModel


class DoctorlessAreaLocationResponse(BaseModel):
    latitude: float | None
    longitude: float | None


class DoctorlessAreaResponse(BaseModel):
    doctorless_city_id: int
    municipality_id: int
    municipality_name: str | None
    city_raw_id: int
    city_name: str | None
    doctorless_flag: bool | None
    location: DoctorlessAreaLocationResponse


class DoctorlessAreaListMetaResponse(BaseModel):
    limit: int
    count: int


class DoctorlessAreasResponse(BaseModel):
    meta: DoctorlessAreaListMetaResponse
    data: list[DoctorlessAreaResponse]
