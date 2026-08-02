export interface Department {
  department_id: number;
  department_name: string;
}

export interface Clinic {
  clinic_id: number;
  clinic_name: string;
  clinic_postcode: string;
  clinic_address: string;
  clinic_tel: string;
  opening_date: string;
  establisher: string;
  general_bed: number | null;
  recuperation_bed: number | null;
  remarks: string;
  signpost_flag: boolean | null;
  location: {
    latitude: number;
    longitude: number;
  };
  departments: Department[];
}

export interface ApiResponse {
  meta: {
    limit: number;
    count: number;
  };
  departments: Department[];
  data: Clinic[];
}