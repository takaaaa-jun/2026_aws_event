import { useState, useEffect } from 'react'
import type { Department, Clinic } from '../types/clinic'
import { fetchDepartments, fetchClinics } from '../api/departments'

interface UseClinicDataResult {
  departments: Department[]
  clinics: Clinic[]
  loading: boolean
  error: string | null
}

// APIを1回だけ呼んで診療科一覧・診療所一覧を両方取得するカスタムフック
// FilterPanel と MapArea で同じデータを共有するために App.tsx で使用する
function useClinicData(): UseClinicDataResult {
  const [departments, setDepartments] = useState<Department[]>([])
  const [clinics, setClinics] = useState<Clinic[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        setLoading(true)
        setError(null)
        // /api/v1/clinics を1回だけ呼ぶ（departments と data を同時に取得）
        const [depts, clinicList] = await Promise.all([
          fetchDepartments(),
          fetchClinics(),
        ])
        if (!cancelled) {
          setDepartments(depts)
          setClinics(clinicList)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : '不明なエラーが発生しました')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    load()

    return () => {
      cancelled = true
    }
  }, [])

  return { departments, clinics, loading, error }
}

export default useClinicData
