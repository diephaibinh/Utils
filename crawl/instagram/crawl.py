from datetime import datetime
import time

from core import crawl, append_to_csv, read_csv, get_crawl_permission
from crawl_info import (
    get_following,
    get_follow_count,
    FOLLOWER_COUNT_PATH,
    FOLLOWER_COUNT_CSV_HEADERS,
    FOLLOWING_LIST_PATH,
    FOLLOWING_PATH
)
from user_info import USER, CRAWL_TYPE_FOLLOWER_COUNT, CRAWL_TYPE_FOLLOWING


class FollowerCount:
    CRAWL_TYPE = CRAWL_TYPE_FOLLOWER_COUNT

    @staticmethod
    def get_stored_followers_count_path(user_info, root: str = FOLLOWER_COUNT_PATH):
        return f"{root}/{user_info['name']}_{user_info['id']}_follower_count.txt"

    def execute(self):
        for name, info in USER.items():
            if not get_crawl_permission(info, self.CRAWL_TYPE):
                continue
            try:
                user_name = info["name"]
                crawl_info = get_follow_count(user_name)
                crawled_data = crawl(crawl_info["method"], crawl_info["request"])
                user_data = crawled_data["data"]["user"]
                data = {key: user_data.get(key) for key in FOLLOWER_COUNT_CSV_HEADERS}
                data["created"] = datetime.now().isoformat()
                append_to_csv(
                    file_path=self.get_stored_followers_count_path(user_info=info),
                    headers=FOLLOWER_COUNT_CSV_HEADERS,
                    data=data,
                )
                time.sleep(crawl_info["delay_time_second"])
            except Exception as e:
                print(str(e))


class Following:
    CRAWL_TYPE = CRAWL_TYPE_FOLLOWING
    PK_KEY = "id"
    API_VALID_KEY = [PK_KEY, "username"]
    STORE_HEADERS = ["created", "unfollow", "new_follow"]

    @staticmethod
    def get_stored_list_following_path(user_info: dict, root: str = FOLLOWING_LIST_PATH):
        return f"{root}/{user_info['name']}_{user_info['id']}_following_list.txt"

    @staticmethod
    def get_stored_following_activity_path(user_info: dict, root: str = FOLLOWING_PATH):
        return f"{root}/{user_info['name']}_{user_info['id']}_following.txt"

    @staticmethod
    def get_following_count(name) -> int:
        follow_count_info = get_follow_count(name)
        follow_count_data = crawl(follow_count_info["method"], follow_count_info["request"])
        return follow_count_data["data"]["user"]["following_count"]

    @staticmethod
    def get_new_following(previous_following_ids: list[str], current_following_ids: list[str]) -> set[str]:
        return set(current_following_ids).difference(set(previous_following_ids))

    @staticmethod
    def get_unfollow(previous_following_ids: list[str], current_following_ids: list[str]) -> set[str]:
        return set(previous_following_ids).difference(set(current_following_ids))

    @staticmethod
    def get_stored_list_following(following) -> list[dict]:
        return [following[key] for key in following]

    def crawl_following(self, user_info: dict) -> tuple[str, dict] | tuple[None, None]:
        if not get_crawl_permission(user_info, self.CRAWL_TYPE):
            return None, None
        try:
            created = datetime.now().isoformat()
            users_by_id: dict = {}

            after = None
            while True:
                following = get_following(user_id=user_info["id"], after=after)
                crawled_data = crawl(following["method"], following["request"])
                users_data = crawled_data["data"]["user"]["edge_follow"]["edges"]
                users_dict = {
                    user["node"]["id"]: {key: user["node"][key] for key in self.API_VALID_KEY}
                    for user in users_data
                }
                users_by_id = {**users_by_id, **users_dict}

                page_info = crawled_data["data"]["user"]["edge_follow"]["page_info"]
                if not page_info["has_next_page"] or not page_info["end_cursor"]:
                    break
                after = page_info["end_cursor"]
                time.sleep(following["delay_time_second"])

            return created, users_by_id

        except Exception as e:
            print(str(e))

    def store_list_following(self, following_users: list[dict], stored_path: str):
        if following_users is None:
            return
        append_to_csv(file_path=stored_path, headers=self.API_VALID_KEY, data=following_users, mode="w")

    def store_following_activity(
            self, created: str, unfollow_ids, new_following_ids, previous_following, current_following, stored_path
    ):
        write_data = {key: "" for key in self.STORE_HEADERS}
        if unfollow_ids:
            write_data["unfollow"] = (
                " || ".join(
                    f"{previous_following[i]['username']} {previous_following[i][self.PK_KEY]}"
                    for i in unfollow_ids
                )
            )
        if new_following_ids:
            write_data["new_follow"] = (
                " || ".join(
                    f"{current_following[i]['username']} {current_following[i][self.PK_KEY]}"
                    for i in new_following_ids
                )
            )

        write_data["created"] = created
        append_to_csv(file_path=stored_path, headers=self.STORE_HEADERS, data=write_data)

    def execute(self):
        for name, info in USER.items():
            try:
                created, current_following = self.crawl_following(info)
                if current_following is None:
                    continue

                previous_following: dict = read_csv(
                    file_path=self.get_stored_list_following_path(info),
                    headers=self.API_VALID_KEY,
                )
                previous_following_ids: list = [previous_following[key][self.PK_KEY] for key in previous_following]
                current_following_ids: list = [current_following[key][self.PK_KEY] for key in current_following]

                self.store_following_activity(
                    created=created,
                    unfollow_ids=self.get_unfollow(previous_following_ids, current_following_ids),
                    new_following_ids=self.get_new_following(previous_following_ids, current_following_ids),
                    previous_following=previous_following,
                    current_following=current_following,
                    stored_path=self.get_stored_following_activity_path(info)
                )
                self.store_list_following(
                    following_users=self.get_stored_list_following(current_following),
                    stored_path=self.get_stored_list_following_path(info)
                )

            except Exception as e:
                print(e)
