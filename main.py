import json
import os
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)

STORAGE_FILE = "visitors.json"


def read_file(file_name):
    if os.path.exists(STORAGE_FILE):
        with open(file_name, "r") as f:
            data = f.read()
            return json.loads(data)
    else:
        return []


def write_to_file(filename, ip_list):
    with open(filename, "w") as f:
        content = json.dumps(ip_list)
        f.write(content)


def store_data(ip, current_datetime):
    visitors: list = read_file(STORAGE_FILE)
    visitors.append({"ip": ip, "datetime": current_datetime})
    write_to_file(STORAGE_FILE, visitors)


# health check route
@app.route("/health")
def health():
    return {"status": "ok"}


# health check route
@app.route("/")
def visit():
    client_ip = request.remote_addr
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    store_data(client_ip, current_datetime_string)
    return {"status": "ok"}


@app.route("/visitors")
def list_visitors():
    visits = read_file(STORAGE_FILE)
    # Sort by datetime in reverse order
    sorted_data = sorted(
        visits,
        key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )
    return {"data": sorted_data}


if __name__ == "__main__":
    app.run()
