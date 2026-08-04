export interface DoctorlessArea {
  doctorless_city_id: number;
  municipality_id: number;
  municipality_name: string;
  city_raw_id: number;
  city_name: string;
  doctorless_flag: boolean;
  location: {
    latitude: number;
    longitude: number;
  };
}

export interface DoctorlessApiResponse {
  meta: {
    limit: number;
    count: number;
  };
  data: DoctorlessArea[];
}
