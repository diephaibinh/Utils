import os
import csv
import json
import requests
from datetime import datetime

from user_info import CRAWL_TIME_TYPE_ALWAYS, USER, CRAWL_TYPE_FOLLOWING


def crawl(method, craw_info):
    if method == "get":
        response = requests.get(**craw_info)
    elif method == "post":
        response = requests.post(**craw_info)
    else:
        return None

    try:
        return response.json()
    except Exception:
        return None


def append_to_csv(file_path, headers, data: dict | list, mode: str = "a"):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode=mode, newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists or mode == "w":
            writer.writeheader()

        writer.writerow(data) if isinstance(data, dict) else writer.writerows(data)


def read_csv(file_path, headers, pk_key="id") -> dict:
    with open(file_path, mode='r', newline='', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, fieldnames=headers)
        rows = [row for row in csv_reader]
        rows.pop(0)  # Exclude header
        users_data_dict: dict = {
            data.get(pk_key): {key: data.get(key) for key in headers}
            for data in rows
        }
        return users_data_dict


def get_crawl_permission(user_info, crawl_type):
    if user_info["permissions"][crawl_type]["permission_type"] == CRAWL_TIME_TYPE_ALWAYS:
        return True

    now = datetime.now()
    times = user_info["permissions"][crawl_type]["time"]
    for start, end in times:
        start_time = datetime.combine(
            date=now.date(),
            time=datetime.strptime(start, "%H:%M").time()
        )
        end_time = datetime.combine(
            date=now.date(),
            time=datetime.strptime(end, "%H:%M").time()
        )
        if start_time <= now <= end_time:
            return True

    return False


def convert_payload_to_dict():
    a = """av: 17841400687084360
    __d: www
    __user: 0
    __a: 1
    __req: 1
    __hs: 19950.HYP:instagram_web_pkg.2.1..0.1
    dpr: 1
    __ccg: UNKNOWN
    __rev: 1015694787
    __s: vplxph:7swzdg:vkq4sm
    __hsi: 7403265988553506321
    __dyn: 7xe5WwlEnwn8K2Wmm1twpUnwgU7S6EeUaUco38w5ux609vCwjE1xoswaq0yE462m0nS4oaEd86a3a0EA2C0iK0D82YK0EUjwGzEaE2iw8O0zEnwhE3fw5rwSyES1Twoob82ZwrUdUbGw4mwr86C1mwrd6goK10xKi2K7E5yqcxK2K1ew
    __csr: gaYQAh6h5Yv5mxGEAL9AHiltVJlbj-HAcBm9X9BjCBOaHD8qG_ApfHF24LGUBaQWF4Ot1CF9vAzvrDamWUgzEOgyBqjgRadAUyCcz8zKGyBCAWG9h5hp99VHy8nzkaDWBCKFqDhuV9FA68-8mEHwyF5K68K8w04CtJ4wSCgC0bVwfu0BVE2tBkPwhUZo1YobemeyAE6yyw0BbzU5O2i4IwS4zzC7oVafyQ6F7gb84nIo0n-0wMy9JyoswCIC1LBx22i2k8ypE4K9x-dwBwNw9904BzU42a4iw0Yvw0kq8
    __comet_req: 7
    fb_dtsg: NAcNDK_kHOKtPF3o975SQPoU8nXAJlL9PiyEZbfcT-XFZMvA84_oauA:17864721031021537:1722144395
    jazoest: 26060
    lsd: 4n6SmehB4sMfBPBp3R8ths
    __spin_r: 1015694787
    __spin_b: trunk
    __spin_t: 1723707185
    fb_api_caller_class: RelayModern
    fb_api_req_friendly_name: PolarisProfilePageContentDirectQuery
    variables: {"id":"5518975262","render_surface":"PROFILE"}
    server_timestamps: true
    doc_id: 8974187929275820"""

    payload_dict = {}
    lines = a.strip().splitlines()

    for line in lines:
        key, value = line.split(":", 1)  # Split by the first occurrence of ":"
        key = key.strip()  # Remove any surrounding whitespace from the key
        value = value.strip()  # Remove any surrounding whitespace from the value
        # If the value is a JSON string, we can parse it into a dictionary
        if value.startswith("{") and value.endswith("}"):
            value = json.loads(value)
        payload_dict[key] = value

    json.dump(payload_dict, open("abc.json", "w", encoding="utf-8"))
