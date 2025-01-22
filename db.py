import mariadb
import os

FETCH_PERMS = (
    "SELECT "
    "uuid, permission "
    "FROM "
    "luckperms_user_permissions "
    "WHERE "
    "permission in ('group.donort0', 'group.donort1', 'group.donort2', 'group.donort3');"
)

FETCH_NAMES = "SELECT name, uuid FROM donor_api_names;"

INSERT_NAMES = "INSERT INTO donor_api_names (uuid, name) VALUES (?, ?);"


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
