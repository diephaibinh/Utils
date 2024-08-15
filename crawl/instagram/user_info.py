CRAWL_TYPE_FOLLOWER_COUNT = "follower_count"
CRAWL_TYPE_FOLLOWING = "following"

CRAWL_TIME_TYPE_ALWAYS = "ALWAYS"
CRAWL_TIME_TYPE_TIME = "TIME"


USER = {
    "carlos_alcaraz": {
        "id": 3227641356,
        "name": "carlos_alcaraz",
        "crawl_list": False,
        "permissions": {
            CRAWL_TYPE_FOLLOWER_COUNT: {
                "permission_type": CRAWL_TIME_TYPE_ALWAYS,
                "time": None,
            },
            CRAWL_TYPE_FOLLOWING: {
                "permission_type": CRAWL_TIME_TYPE_TIME,
                "time": [("00:00", "00:15"), ("18:00", "18:15")],
            }
        },
    },
    "lionel_messi": {
        "id": 427553890,
        "name": "lionel_messi",
        "crawl_list": False,
        "permissions": {
            CRAWL_TYPE_FOLLOWER_COUNT: {
                "permission_type": CRAWL_TIME_TYPE_ALWAYS,
                "time": None,
            },
            CRAWL_TYPE_FOLLOWING: {
                "permission_type": CRAWL_TIME_TYPE_TIME,
                "time": [("00:00", "00:15"), ("18:00", "18:15")],
            }
        },
    },
    "cristiano_ronaldo": {
        "id": 173560420,
        "name": "cristiano_ronaldo",
        "crawl_list": False,
        "permissions": {
            CRAWL_TYPE_FOLLOWER_COUNT: {
                "permission_type": CRAWL_TIME_TYPE_ALWAYS,
                "time": None,
            },
            CRAWL_TYPE_FOLLOWING: {
                "permission_type": CRAWL_TIME_TYPE_TIME,
                "time": [("00:00", "00:15"), ("18:00", "18:15")],
            }
        },
    },
    "duc_phat": {
        "id": 5518975262,
        "name": "duc_phat",
        "crawl_list": False,
        "permissions": {
            CRAWL_TYPE_FOLLOWER_COUNT: {
                "permission_type": CRAWL_TIME_TYPE_ALWAYS,
                "time": None,
            },
            CRAWL_TYPE_FOLLOWING: {
                "permission_type": CRAWL_TIME_TYPE_TIME,
                "time": [
                    ("00:00", "00:15"),
                    ("08:00", "08:15"),
                    ("12:00", "12:15"),
                    ("16:00", "16:15"),
                    ("20:00", "20:15"),
                ],
            }
        },
    }
}
