# Dockerを用いた，環境差分をなくした環境構築
- コンテナを作成して，ローカル差分をなくすことで，環境の構築を素早く行うことができる．

## 作成するコンテナ

### dbコンテナ
- イメージ: mysql:8.0
- ポート番号: 3306
- データベースの保存先: /var/lib/mysql
  - "mysql_data"と名前を付けて，永続化（再起動してもデータが残る）

### backendコンテナ
- イメージ: python:3.14.6-slim
- ポート番号: 8000

### frontendコンテナ
- イメージ: node:20-alpine
- ポート番号: 5173

## docker-compose.yamlとDockerfileの違い
- docker-compose.yaml: 複数コンテナの連携
- Dockerfile: 1コンテナ分の設定

## 初回セットアップ手順

```bash
# backendコンテナにアクセスして，データベースの読み込みを行う
# データベースのテーブル作成
docker compose exec backend python database/scripts/init_db.py
# ジオコーディングデータ等のCSVデータインポート
docker compose exec backend python database/scripts/import_data.py
```


## 各コンテナへのアクセス方法

| サービス | コンテナ内ポート | ホストPCからのアクセスURL / 接続先 |
| :--- | :--- | :--- |
| **フロントエンド** (Vite + React + TS) | `5173` | [http://localhost:5173](http://localhost:5173) |
| **バックエンド** (FastAPI) | `8000` | [http://localhost:8000](http://localhost:8000) (API仕様書: [http://localhost:8000/docs](http://localhost:8000/docs)) |
| **データベース** (MySQL) | `3306` | ホスト: `localhost` / ポート: `3306`（`.env` の `MYSQL_PORT` に従う） |

---

## 各コンテナのバージョン確認コマンド

コンテナが起動している状態で、ホストPC（Windows）のターミナルから以下のコマンドを実行することで、各環境のバージョンを確認できます。

### 1. データベース (MySQL) のバージョン確認
```bash
docker compose exec db mysql --version

# コンテナ内に入るとき
docker compose exec db bash
mysql -u root -p
# pass
```

### 2. バックエンド (Python) のバージョン確認
```bash
docker compose exec backend python --version

# コンテナ内に入るとき
docker compose exec backend bash
```

### 3. フロントエンド (Node.js) のバージョン確認
```bash
docker compose exec frontend node --version

# コンテナ内に入るとき
docker compose exec frontend bash
```

---

## Docker Compose 起動・操作用基本コマンド

開発時に使用する Docker Compose の基本操作コマンドです。プロジェクトのルートディレクトリで実行します。

### 1. 起動（バックグラウンド実行）
初回起動や、通常起動の際に使用します。
```bash
docker compose up -d
```

### 2. 再ビルドを伴う起動
`requirements.txt` や `package.json` を変更した際や、Dockerfileを変更した後に使用します。
```bash
docker compose up --build -d
```

### 3. 停止
起動しているすべてのコンテナを停止・削除します（ボリューム内のデータベースデータは保護されます）。
```bash
docker compose down
```

### 4. ログの確認
コンテナ内のログをリアルタイムで監視したい場合に使用します。
```bash
docker compose logs -f
```

### 5. コンテナの稼働ステータス確認
```bash
docker compose ps
```