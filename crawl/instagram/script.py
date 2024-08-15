import os
import csv

from user_info import USER
from crawl_info import FOLLOWING_LIST_PATH, FOLLOWER_COUNT_PATH, FOLLOWING_PATH
from crawl import Following, FollowerCount
from core import append_to_csv


for path in (FOLLOWER_COUNT_PATH, FOLLOWING_PATH, FOLLOWING_LIST_PATH):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

messi = "/home/EcourseBE/media/crawl/messi.txt"
alcaraz = "/home/EcourseBE/media/crawl/alcaraz.txt"
ronaldo = "/home/EcourseBE/media/crawl/ronaldo.txt"
headers = ["created", "pk", "username", "category", "follower_count", "following_count", "media_count"]
new_headers = ["created", "follower_count", "following_count", "media_count"]

# Follower count
follower = FollowerCount()
for path, user_info in ((messi, USER["lionel_messi"]), (alcaraz, USER["carlos_alcaraz"]), (ronaldo, USER["cristiano_ronaldo"])):
    with open(path, mode='r', newline='', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, fieldnames=headers)
        rows = [row for row in csv_reader]
        rows.pop(0)  # Exclude header

        new_data = [{key: row.get(key) for key in new_headers} for row in rows]
        new_path = follower.get_stored_followers_count_path(user_info)
        append_to_csv(new_path, new_headers, new_data, "w")

        os.remove(path)


# Following
following = Following()
for name, info in USER.items():
    if not info.get("crawl_list"):
        continue

    _, current_following = following.crawl_following(info)
    following.store_list_following(
        following_users=following.get_stored_list_following(current_following),
        stored_path=following.get_stored_list_following_path(info)
    )
