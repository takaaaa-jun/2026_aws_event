# データベースの作成・起動手順書

## 1. 仮想環境の作成と有効化
Pythonの実行環境として `dbenv` を作成し有効化します。

```bash
cd database
# 仮想環境の作成 (初回のみ実行)
python -m venv dbenv

# 仮想環境の有効化 (毎回実行)
dbenv\Scripts\activate
```

## 2. 必要なライブラリのインストール
必要な依存パッケージ（SQLAlchemy、dotenv、pymysql等）をインストールします。

```bash
pip install -r requirements.txt
```

## 3. ローカルデータベース (MySQL) の起動
Docker Compose を使用して、ローカルPC上にデータベース（MySQL）を起動します。プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
# コンテナの起動
docker compose up -d
```

## 4. テーブルの作成・初期化
モデル定義に基づいて、データベース内に自動でテーブルを作成する初期化スクリプトを実行します。
※実行する前に `.env` の `MYSQL_HOST` が `localhost` になっていることを確認してください。

```bash
python scripts/init_db.py
```

## 5. データのインポート
CSVファイル（一般・歯科クリニックのジオコーディングデータ）をデータベースにインポートします。

```bash
python scripts/import_data.py
```

## 6. 作成されたデータ・テーブルの確認方法
Docker Compose を通じてコンテナ内のMySQLクライアントを呼び出し、データが正常に登録されているかを確認できます。

### テーブル一覧の確認
```bash
docker compose exec db mysql -u root -ppass -e "SHOW TABLES FROM clinic;"
```

### 登録されたデータの確認（件数確認）
```bash
docker compose exec db mysql -u root -ppass -D clinic -e "SELECT COUNT(*) FROM clinic;"
```

### インタラクティブモードでのログイン
```bash
docker compose exec db mysql -u root -p
```