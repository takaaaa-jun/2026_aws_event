import { useState, useMemo } from 'react'
import Header from './components/Header'
import FilterPanel from './components/FilterPanel'
import MapArea from './components/MapArea'
import useClinicData from './hooks/useClinicData'
import useDoctorlessAreas from './hooks/useDoctorlessAreas'
import './App.css'

function App() {
  const [selectedDepartments, setSelectedDepartments] = useState<number[]>([])
  const [showDoctorlessArea, setShowDoctorlessArea] = useState<boolean>(false)

  // APIを1回だけ呼んで departments と clinics を取得
  // FilterPanel と MapArea に配布する
  const { departments, clinics, loading, error } = useClinicData()
  
  // 無医地区データの取得
  const { areas: doctorlessAreas } = useDoctorlessAreas()

  // 選択中の診療科で診療所を絞り込み → MapArea(田部君)に渡す
  const filteredClinics = useMemo(() => {
    if (selectedDepartments.length === 0) {
      return [] // 何も選択されていない時は0件表示にする
    }
    return clinics.filter((clinic) =>
      clinic.departments.some((dep) => selectedDepartments.includes(dep.department_id))
    )
  }, [clinics, selectedDepartments])

  return (
    <div className="app">
      <Header />
      <div className="app-body">
        {/* 田部君はここで filteredClinics を使う */}
        <MapArea 
          clinics={filteredClinics} 
          doctorlessAreas={showDoctorlessArea ? doctorlessAreas : []}
        />

        {/* フィルターパネル: departments は App から受け取る*/}
        <FilterPanel
          departments={departments}
          loading={loading}
          error={error}
          selected={selectedDepartments}
          onChange={setSelectedDepartments}
          showDoctorlessArea={showDoctorlessArea}
          onToggleDoctorlessArea={setShowDoctorlessArea}
        />
      </div>
    </div>
  )
}

export default App