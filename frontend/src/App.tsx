import { useState, useMemo } from 'react'
import Header from './components/Header'
import FilterPanel from './components/FilterPanel'
import MapArea from './components/MapArea'
import useClinicData from './hooks/useClinicData'
import './App.css'

function App() {
  const [selectedDepartments, setSelectedDepartments] = useState<number[]>([])

  // APIを1回だけ呼んで departments と clinics を取得
  // → FilterPanel と MapArea に配布する
  const { departments, clinics, loading, error } = useClinicData()

  // 選択中の診療科で診療所を絞り込み → MapArea（Googleマップ担当）に渡す
  const filteredClinics = useMemo(() => {
    if (selectedDepartments.length === 0) {
      return clinics
    }
    return clinics.filter((clinic) =>
      clinic.departments.some((dep) => selectedDepartments.includes(dep.department_id))
    )
  }, [clinics, selectedDepartments])

  return (
    <div className="app">
      <Header />
      <div className="app-body">
        {/* Googleマップ担当の方はここで filteredClinics を使う */}
        <MapArea clinics={filteredClinics} />

        {/* フィルターパネル: departments は App から受け取る（API二重呼び出しなし） */}
        <FilterPanel
          departments={departments}
          loading={loading}
          error={error}
          selected={selectedDepartments}
          onChange={setSelectedDepartments}
        />
      </div>
    </div>
  )
}

export default App