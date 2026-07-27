# Node.jsのバージョン指定
FROM node:20-alpine

# 作業ディレクトリの指定
# frontendコンテナ内の /app は， /2026_aws_event/frontend に対応
WORKDIR /app

# パッケージ定義ファイルをコンテナにコピー
# package.json と package-lock.json (存在する場合) を先にコピーしてキャッシュを有効化
COPY package*.json ./

# 依存パッケージのインストール
RUN npm install

# ソースコード全体をコンテナにコピー
COPY . .

# Vite のデフォルト開発ポート（5173番）を開放
EXPOSE 5173

# 開発用サーバーの起動コマンド
# コンテナ起動時に「npm run dev」を実行し、ホスト（0.0.0.0）をバインドして外部からアクセス可能にする
CMD ["npm", "run", "dev", "--", "--host"]
