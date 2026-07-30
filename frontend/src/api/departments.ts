import type { ApiResponse, Department } from '../types/clinic'
import { DEPARTMENTS } from '../constants/departments'

const API_BASE_URL = 'http://localhost:8000'

// バックエンドAPIが未完成の場合は true にしてモックを使う
const MOCK_MODE = true

// 診療科一覧を取得する（APIレスポンスの departments フィールドを返す）
export async function fetchDepartments(): Promise<Department[]> {
  if (MOCK_MODE) {
    // モック: constants の43科リストをそのまま返す
    return Promise.resolve(DEPARTMENTS)
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/departments`)
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

  const response = await fetch(`${API_BASE_URL}/api/v1/departments`)
  if (!response.ok) {
    throw new Error(`診療所一覧の取得に失敗しました: ${response.status}`)
  }
  const json: ApiResponse = await response.json()
  return json.data
}
