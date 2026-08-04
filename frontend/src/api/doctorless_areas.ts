import type { DoctorlessApiResponse, DoctorlessArea } from '../types/doctorlessArea'

const API_BASE_URL = ''

// limit = 3000 に設定して全件取得
const DOCTORLESS_ENDPOINT = `${API_BASE_URL}/api/v1/doctorless_area?limit=3000`

export async function fetchDoctorlessAreas(): Promise<DoctorlessArea[]> {
  const response = await fetch(DOCTORLESS_ENDPOINT)
  if (!response.ok) {
    throw new Error(`無医地区の取得に失敗しました: ${response.status}`)
  }
  const json: DoctorlessApiResponse = await response.json()
  return json.data
}
