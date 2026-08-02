import { useState, useEffect } from 'react'
import type { Department } from '../types/clinic'
import { fetchDepartments } from '../api/departments'

interface UseDepartmentsResult {
  departments: Department[]
  loading: boolean
  error: string | null
}

// 診療科一覧をAPIから取得するカスタムフック
function useDepartments(): UseDepartmentsResult {
  const [departments, setDepartments] = useState<Department[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        setLoading(true)
        setError(null)
        const data = await fetchDepartments()
        if (!cancelled) {
          setDepartments(data)
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

  return { departments, loading, error }
}

export default useDepartments
