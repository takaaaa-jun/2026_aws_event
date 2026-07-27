# Pythonのバージョン指定
FROM python:3.14.6-slim

# 作業ディレクトリの指定
# backendのコンテナ内の /appは，/2026_aws_event/backend に対応
WORKDIR /app

# システムのアップデートと必要なパッケージのインストール
RUN apt-get update \
    # build-essentialは、C言語のコンパイルなど、Pythonの拡張モジュールをビルドする際に必要になるツール
    && apt-get install -y --no-install-recommends build-essential \
    # パッケージリストのキャッシュを削除することで、イメージサイズを削減
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコンテナにコピー
# requirements.txtが変更されたときにライブラリの更新が実行されるようになる
COPY requirements.txt .

# 依存パッケージのインストール
# --no-cache-dir: キャッシュを使用しないことで、イメージサイズを削減
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコンテナにコピー
COPY . .

# 8000番ポートを開放
EXPOSE 8000

# アプリケーションの起動コマンド
# コンテナを起動すると，これらのコマンドが実行される
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
