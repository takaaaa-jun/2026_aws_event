import type { ApiResponse, Department } from '../types/clinic'
import { DEPARTMENTS } from '../constants/departments'

const API_BASE_URL = ''

//デザインの確認のため
const MOCK_MODE = false

// 正しいエンドポイント: /api/v1/clinics?limit=<件数>
// limit は必須パラメータ。今回は3000を指定
const CLINICS_ENDPOINT = `${API_BASE_URL}/api/v1/clinics?limit=3000`

// 診療科一覧を取得する（APIレスポンスの departments フィールドを返す）
export async function fetchDepartments(): Promise<Department[]> {
  if (MOCK_MODE) {
    // モック: constants の43科リストをそのまま返す
    return Promise.resolve(DEPARTMENTS)
  }

  const response = await fetch(CLINICS_ENDPOINT)
  if (!response.ok) {
    throw new Error(`診療科一覧の取得に失敗しました: ${response.status}`)
  }
  const json: ApiResponse = await response.json()
  // レスポンスの departments フィールドを返す（data ではない）
  return json.departments
}

// 診療所一覧を取得する（APIレスポンスの data フィールドを返す）
export async function fetchClinics() {
  if (MOCK_MODE) {
    return Promise.resolve([])
  }

  const response = await fetch(CLINICS_ENDPOINT)
  if (!response.ok) {
    throw new Error(`診療所一覧の取得に失敗しました: ${response.status}`)
  }
  const json: ApiResponse = await response.json()
  return json.data
}
