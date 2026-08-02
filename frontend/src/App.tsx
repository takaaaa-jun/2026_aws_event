import GoogleMap from "./components/GoogleMap";
import type { clinicMap } from "./types/clinicMap";
import "./App.css";

// テスト用データ
const clinicMaps: clinicMap[] = [
  {
    id: 1,
    name: "本間医院",
    lat: 38.223648,
    lng: 139.475800,
  },
  {
    id: 2,
    name: "安斎医院",
    lat: 38.192665,
    lng: 139.437790,
  },
  {
    id: 3,
    name: "富樫眼科医院",
    lat: 38.221596,
    lng: 139.476959,
  },
];

function App() {
  return (
    <main className="app">
      <p>マーカーをクリックして緯度経度情報を表示</p>

      <GoogleMap locations={clinicMaps} />
    </main>
  );
}

export default App;