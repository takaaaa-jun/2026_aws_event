import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true, // 5173が使用中の場合はエラーにする
    host: true,       // コンテナ外（Windows側）からアクセス可能にする
    proxy: {
      // /api から始まるリクエストをバックエンドコンテナに転送する
      '/api': {
        target: 'http://backend:8000', // Docker Compose のサービス名で指定
        changeOrigin: true,
      },
    },
  },
})
