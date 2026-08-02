class Logger:
    def start_point(self):
        print("処理を開始しました")

    def end_point(self):
        print("処理を終了しました")

    def error_point(self):
        print("エラーが発生しました")

    def exception_point(self):
        print("例外が発生しました")


class Log_database(Logger):
    def log_database(self):
        super.start_point()
        try:
            sql_query = self._generate_sql_query()
            print(f"SQLクエリ: {sql_query}")
            super.end_point()
        except Exception as e:
            super.error_point()
            super.exception_point()
