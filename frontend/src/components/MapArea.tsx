import type { Clinic } from '../types/clinic'
import type { clinicMap } from '../types/clinicMap'
import type { DoctorlessArea } from '../types/doctorlessArea'
import GoogleMap from './GoogleMap'
import './MapArea.css'

interface MapAreaProps {
  clinics: Clinic[]
  doctorlessAreas?: DoctorlessArea[]
}

function MapArea({ clinics, doctorlessAreas = [] }: MapAreaProps) {
  // Clinicのデータから位置情報を持つものだけを抽出し、GoogleMap用のデータ型に変換する
  const mapLocations: clinicMap[] = clinics
    .filter((clinic) => clinic.location !== null)
    .map((clinic) => ({
      lat: clinic.location!.latitude,
      lng: clinic.location!.longitude,
      name: clinic.clinic_name,
    }))

  return (
    <div className="map-area">
      <GoogleMap locations={mapLocations} doctorlessAreas={doctorlessAreas} />
      <div className="map-info-overlay" style={{ textAlign: 'center', marginTop: '10px' }}>
        <p className="map-selected-info">
          表示中の診療所：{clinics.length} 件 （うち位置情報あり: {mapLocations.length}件）
        </p>
      </div>
    </div>
  )
}

export default MapArea
