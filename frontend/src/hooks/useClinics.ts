import { useState, useEffect } from 'react'
import type { Clinic } from '../types/clinic'
import { fetchClinics } from '../api/departments'

interface UseClinicsResult {
  clinics: Clinic[]
  loading: boolean
  error: string | null
}

// 診療所一覧をAPIから取得するカスタムフック
function useClinics(): UseClinicsResult {
  const [clinics, setClinics] = useState<Clinic[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        setLoading(true)
        setError(null)
        const data = await fetchClinics()
        if (!cancelled) {
          setClinics(data)
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

    // コンポーネントがアンマウントされたときにキャンセルする
    return () => {
      cancelled = true
    }
  }, [])

  return { clinics, loading, error }
}

export default useClinics
