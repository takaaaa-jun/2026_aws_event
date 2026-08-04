import { useEffect, useRef } from "react";
import {
  importLibrary,
  setOptions,
} from "@googlemaps/js-api-loader";

import type { clinicMap } from "../types/clinicMap";
import type { DoctorlessArea } from "../types/doctorlessArea";

// コンポーネントが受けとるデータ型の定義
type GoogleMapProps = {
  locations: clinicMap[];
  doctorlessAreas?: DoctorlessArea[];
};

// マップの中心座標
const NIIGATA_CENTER = {
  lat: 37.916,
  lng: 139.036,
};

// APIキーの設定
setOptions({
  key: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "", // 自身のAPIキーを設定
  v: "weekly", //週単位で更新を読み込む設定
});

// GoogleMapの表示
function GoogleMap({ locations, doctorlessAreas = [] }: GoogleMapProps) {
  // GoogleMapの地図表示部分(HTML)を保存
  const mapElementRef = useRef<HTMLDivElement | null>(null);

  // GoogleMapの本体を保存
  const mapRef = useRef<google.maps.Map | null>(null);

  // マーカーを保存
  const markersRef = useRef<
    google.maps.marker.AdvancedMarkerElement[]
  >([]);

  // 円(Circle)を保存
  const circlesRef = useRef<google.maps.Circle[]>([]);

  useEffect(() => {
    let cancelled = false;

    // マップとマーカーの初期化
    const initializeMapAndMarkers = async () => {
      if (!mapElementRef.current) {
        return;
      }

      // 使用ライブラリの読み込み
      const [mapsLib, markerLib] =
        await Promise.all([
          importLibrary("maps") as Promise<google.maps.MapsLibrary>,
          importLibrary("marker") as Promise<google.maps.MarkerLibrary>,
        ]);
      
      const Map = mapsLib.Map;
      const AdvancedMarkerElement = markerLib.AdvancedMarkerElement;
      // Circleクラスを明示的に取得（新しいGoogle Maps APIのお作法に対応するため）
      const Circle = (mapsLib as any).Circle || google.maps.Circle;

      if (cancelled || !mapElementRef.current) {
        return;
      }

      // 地図が未作成なら作成
      if (!mapRef.current) {
        mapRef.current = new Map(mapElementRef.current, {
          // ズームレベル
          zoom: 10,
          // 中心位置
          center: NIIGATA_CENTER,
          //マップID
          mapId:
            import.meta.env.VITE_GOOGLE_MAP_ID ||
            "DEMO_MAP_ID",
        });
      }

      const map = mapRef.current;

      // 古いマーカーを削除
      markersRef.current.forEach((marker) => {
        marker.map = null;
      });
      markersRef.current = [];

      // 古い円を削除
      circlesRef.current.forEach((circle) => {
        circle.setMap(null);
      });
      circlesRef.current = [];

      // 情報ウィンドウを定義
      const infoWindow = new google.maps.InfoWindow();

      const validLocations = locations.filter(
        (location) =>
          Number.isFinite(location.lat) &&
          Number.isFinite(location.lng),
      );

      // マーカーの作成
      const newMarkers = validLocations.map((location) => {
        const marker = new AdvancedMarkerElement({
          map,
          position: {
            lat: location.lat,
            lng: location.lng,
          },
          title: location.name,
        });

        // マーカーのクリックイベント
        // 表示する情報を編集
        marker.addListener("click", () => {
          infoWindow.setContent(`
            <div>
              <strong>${escapeHtml(location.name)}</strong>
              <br>
              緯度: ${location.lat}
              <br>
              経度: ${location.lng}
            </div>
          `);

          infoWindow.open({
            map,
            anchor: marker,
          });
        });

        return marker;
      });

      markersRef.current = newMarkers;

      // 無医地区の円(Circle)を作成
      // locationデータが存在し、正しい緯度経度を持つものだけを抽出（エラー回避）
      const validAreas = doctorlessAreas.filter(
        (area) =>
          area.location &&
          Number.isFinite(area.location.latitude) &&
          Number.isFinite(area.location.longitude)
      );

      console.log("描画対象の無医地区データ（有効なもの）:", validAreas);

      const newCircles = validAreas.map((area) => {
        const circle = new Circle({
          strokeColor: "#FF0000", // 赤色
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF0000",
          fillOpacity: 0.35,
          map,
          center: { lat: area.location.latitude, lng: area.location.longitude },
          radius: 4000, // 4km (メートル指定)
        });
        return circle;
      });
      
      circlesRef.current = newCircles;
    };

    void initializeMapAndMarkers().catch((error: unknown) => {
      console.error(
        "地図またはマーカーの表示に失敗しました",
        error,
      );
    });

    return () => {
      cancelled = true;

      markersRef.current.forEach((marker) => {
        marker.map = null;
      });
      markersRef.current = [];

      circlesRef.current.forEach((circle) => {
        circle.setMap(null);
      });
      circlesRef.current = [];
    };
  }, [locations, doctorlessAreas]);

  // マップ部分のHTML
  return (
    <div
      ref={mapElementRef}
      // マップ部分のCSS
      style={{
        width: "100%", // MapArea内でレイアウトを制御しやすいように100%に変更
        flex: 1, // 高さを固定せず、余白全体を自動で埋めるように変更
        border: "1px solid #ccc",
      }}
    />
  );
}

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export default GoogleMap;
