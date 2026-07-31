# Node.jsのバージョン指定
FROM node:20-alpine

# 作業ディレクトリの指定
# frontendコンテナ内の /app/frontend は，ホストの ./frontend に対応
WORKDIR /app/frontend

# パッケージ定義ファイルをコンテナにコピー
COPY package*.json ./

# 依存パッケージのインストール
RUN npm install

# ソースコード全体をコンテナにコピー
COPY . .

# Vite のデフォルト開発ポート（5173番）を開放
EXPOSE 5173

# 開発用サーバーの起動コマンド
CMD ["npm", "run", "dev", "--", "--host"]
