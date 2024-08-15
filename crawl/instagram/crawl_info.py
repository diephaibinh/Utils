from payload import COOKIE, USER_FOLLOW_COUNT_PAYLOAD
import json
from urllib.parse import quote

FOLLOWING_URL = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables={VARIABLES}"
FOLLOWING_PATH = "/home/EcourseBE/media/crawl/following"
FOLLOWING_LIST_PATH = "/home/EcourseBE/media/crawl/following/list_following"
FOLLOWING_LIMIT = 50
DELAY_FOLLOWING_TIME_SECOND = 7

FOLLOWER_URL = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={VARIABLES}"


FOLLOWER_COUNT_URL = "https://www.instagram.com/graphql/query"
FOLLOWER_COUNT_PATH = "/home/EcourseBE/media/crawl/follower_count"
DELAY_FOLLOWER_COUNT_SECOND = 3

FOLLOWER_COUNT_CSV_HEADERS = ["created", "follower_count", "following_count", "media_count"]


def get_following(user_id, after: str = None):
    params = {
        "id": user_id,
        "include_reel": False,
        "fetch_mutual": False,
        "first": 50,
        "after": after,
    }

    return {
        "method": "get",
        "request": {
            "url": FOLLOWING_URL.format(VARIABLES=quote(json.dumps(params))),
            "headers": {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": COOKIE,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like, Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-Asbd-Id": "129477",
                "X-Ig-App-Id": "936619743392459",
                "x-Ig-Www-Claim": "hmac.AR0PWZKabuvjMIL61wb-aY9lhShKItT1E_OEenzIcQEks7Iy",
            }
        },
        "time": FOLLOWING_LIMIT,
        "delay_time_second": DELAY_FOLLOWING_TIME_SECOND,
    }


def get_follow_count(name: str):
    return {
        "method": "post",
        "request": {
            "url": FOLLOWER_COUNT_URL,
            "data": USER_FOLLOW_COUNT_PAYLOAD[name],
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": COOKIE,
            },
        },
        "delay_time_second": DELAY_FOLLOWER_COUNT_SECOND,
    }
