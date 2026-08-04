import { useState, useEffect } from 'react'
import type { DoctorlessArea } from '../types/doctorlessArea'
import { fetchDoctorlessAreas } from '../api/doctorless_areas'

export default function useDoctorlessAreas() {
  const [areas, setAreas] = useState<DoctorlessArea[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let ignore = false

    const loadData = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await fetchDoctorlessAreas()
        if (!ignore) {
          setAreas(data)
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : '無医地区のデータ取得に失敗しました')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadData()

    return () => {
      ignore = true
    }
  }, [])

  return { areas, loading, error }
}
