import sys
from pathlib import Path

# utilsディレクトリへのパスをシステムパスに追加して、インポート可能にします
utils_dir = Path(__file__).resolve().parent.parent / "utils"
sys.path.append(str(utils_dir))

from connection_database import connection_database
# models から Base をインポートすることで、テーブルのメタデータが登録された Base を使用できます
from models import Base, Clinic, LatitudeLongitude, Department, ClinicDepartment

def init_tables():
    # 接続情報（engine）のみを connection_database から取得します
    engine, _, _ = connection_database()
    
    # 既存のテーブルをすべて削除して初期化します
    Base.metadata.drop_all(bind=engine)
    # models から読み込んだ Base を使ってテーブルを作成します
    Base.metadata.create_all(bind=engine)
    print("すべてのテーブルの作成・初期化が完了しました。")

if __name__ == "__main__":
    init_tables()
