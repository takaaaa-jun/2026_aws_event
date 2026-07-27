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
