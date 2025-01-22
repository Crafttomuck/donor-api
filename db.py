import mariadb
import os


class DB:
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user=os.environ["DB_USER"],
                password=os.environ["DB_PW"],
                host=os.environ["DB_HOST"],
                port=int(os.environ["DB_PORT"]),
                database="minecraft",
            )
        except mariadb.Error as e:
            raise RuntimeError(f"Error connecting to MariaDB Platform: {e}")

    def __enter__(self, *args, **kwargs) -> mariadb.Cursor:
        return self.conn.cursor()

    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        self.conn.close()
