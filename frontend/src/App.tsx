import { useState, useMemo } from 'react'
import Header from './components/Header'
import FilterPanel from './components/FilterPanel'
import MapArea from './components/MapArea'
import type { Clinic } from './types/clinic'
import './App.css'

function App() {
  const [selectedDepartments, setSelectedDepartments] = useState<number[]>([])
  // clinics は MapArea 担当の方が API から取得する想定
  // 現時点では空配列、API 実装後に useClinics フックなどで差し替える
  const [clinics] = useState<Clinic[]>([])

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
        {/* Google Maps 担当の方には「絞り込み済みの配列」だけを渡す */}
        <MapArea clinics={filteredClinics} />

        <FilterPanel
          selected={selectedDepartments}
          onChange={setSelectedDepartments}
        />
      </div>
    </div>
  )
}

export default App