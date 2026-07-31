import { useEffect, useRef } from "react";
import {
  importLibrary,
  setOptions,
} from "@googlemaps/js-api-loader";

import type { clinicMap } from "../types/clinicMap";

// コンポーネントが受けとるデータ型の定義
type GoogleMapProps = {
  locations: clinicMap[];
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
function GoogleMap({ locations }: GoogleMapProps) {
  // GoogleMapの地図表示部分(HTML)を保存
  const mapElementRef = useRef<HTMLDivElement | null>(null);

  // GoogleMapの本体を保存
  const mapRef = useRef<google.maps.Map | null>(null);

  // マーカーを保存
  const markersRef = useRef<
    google.maps.marker.AdvancedMarkerElement[]
  >([]);

  useEffect(() => {
    let cancelled = false;

    // マップとマーカーの初期化
    const initializeMapAndMarkers = async () => {
      if (!mapElementRef.current) {
        return;
      }

      // 使用ライブラリの読み込み
      const [{ Map }, { AdvancedMarkerElement }] =
        await Promise.all([
          importLibrary("maps") as Promise<google.maps.MapsLibrary>,
          importLibrary("marker") as Promise<google.maps.MarkerLibrary>,
        ]);

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
    };
  }, [locations]);

  // マップ部分のHTML
  return (
    <div
      ref={mapElementRef}
      // マップ部分のCSS
      style={{
        width: "100%", // MapArea内でレイアウトを制御しやすいように100%に変更
        height: "600px",
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
