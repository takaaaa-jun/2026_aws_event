import type { Clinic } from '../types/clinic'
import './MapArea.css'

interface MapAreaProps {
  clinics: Clinic[]
}

function MapArea({ clinics }: MapAreaProps) {
  return (
    <div className="map-area">
      {/* Google Maps API キー取得後にここを実装する */}
      <div className="map-placeholder">
        <div className="map-placeholder-inner">
          <svg
            className="map-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            aria-hidden="true"
          >
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />
            <circle cx="12" cy="9" r="2.5" />
          </svg>
          <p className="map-placeholder-text">地図表示エリア</p>
          <p className="map-placeholder-sub">
            Google Maps API キーを設定すると地図が表示されます
          </p>
          {clinics.length > 0 && (
            <p className="map-selected-info">
              表示中の診療所：{clinics.length} 件
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default MapArea
