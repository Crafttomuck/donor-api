import requests
import logging
import db
from flask import Flask
from mariadb import Error as MariaError

app = Flask(__name__)

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route("/")
def get_donor_info():
    raw_data = {}
    data = {"t0": [], "t1": [], "t2": [], "t3": []}
    with db.DB() as cur:
        app.logger.info("Fetching perms")
        cur.execute(db.FETCH_PERMS)
        for uuid, permission in cur:
            tier = permission[-2:]
            raw_data[uuid] = tier
        app.logger.info("Fetching names")
        cur.execute(db.FETCH_NAMES)
        for name, uuid in cur:
            if uuid not in raw_data.keys():
                continue
            tier = raw_data[uuid]
            data[tier].append(name)
            del raw_data[uuid]
        to_insert = {}
        app.logger.info(f"Fetching usernames for new uuids {raw_data.keys()}")
        for uuid, tier in raw_data.items():
            response = requests.get("https://api.minetools.eu/uuid/" + uuid)
            if response.status_code != 200:
                print(
                    f"Error fetching name for UUID {uuid}, code {response.status_code}"
                )
                continue
            name = response.json()["name"]
            data[tier].append(name)
            to_insert[uuid] = name
        for uuid, name in to_insert.items():
            app.logger.info(f"Inserting {uuid}: {name}")
            try:
                cur.execute(db.INSERT_NAMES, (uuid, name))
            except MariaError as e:
                app.logger.error(e)

    return data
