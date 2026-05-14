"""
Fetch a Reddit user's public activity (posts & comments) via the JSON API.

No authentication required — uses the public ``.json`` endpoints.
"""

import json
import time
import urllib.request

from .utils import clean, ts


_USER_AGENT = "reddit-graph/1.0"
_PAGE_SIZE = 25


def _fetch_json(url: str) -> dict | None:
    """GET *url* and return parsed JSON, or ``None`` on any HTTP/network error."""
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


def _parse_comment(d: dict) -> dict:
    """Extract the fields we care about from a ``t1`` (comment) listing child."""
    return {
        "type": "comment",
        "id": d["id"],
        "subreddit": d["subreddit"],
        "created": ts(d["created_utc"]),
        "score": d["score"],
        "controversial": d["controversiality"] == 1,
        "is_own_post": d["is_submitter"],
        "edited": d["edited"] is not False,
        "body": clean(d["body"].strip()),
        "post_title": clean(d["link_title"]),
        "permalink": "https://reddit.com" + d["permalink"],
    }


def _parse_post(d: dict) -> dict:
    """Extract the fields we care about from a ``t3`` (post) listing child."""
    return {
        "type": "post",
        "id": d["id"],
        "subreddit": d["subreddit"],
        "created": ts(d["created_utc"]),
        "title": clean(d["title"]),
        "body": clean(d.get("selftext", "").strip()),
        "score": d["score"],
        "upvote_ratio": d.get("upvote_ratio", 0),
        "num_comments": d["num_comments"],
        "flair": clean(d.get("link_flair_text") or ""),
        "edited": d["edited"] is not False,
        "permalink": "https://reddit.com" + d["permalink"],
    }


def fetch_all_activity(username: str) -> list[dict]:
    """
    Page through ``/user/{username}.json`` and return every post & comment
    as a list of normalised dicts.
    """
    all_items: list[dict] = []
    after = ""
    page = 1

    while True:
        print(f"  Fetching page {page}...")
        url = (
            f"https://www.reddit.com/user/{username}.json"
            f"?limit={_PAGE_SIZE}&after={after}"
        )
        data = _fetch_json(url)
        if not data:
            break

        batch: list[dict] = []
        for child in data["data"]["children"]:
            kind = child["kind"]
            d = child["data"]
            if kind == "t1":
                batch.append(_parse_comment(d))
            elif kind == "t3":
                batch.append(_parse_post(d))

        if not batch:
            break

        all_items.extend(batch)
        after = data["data"].get("after") or ""
        if not after:
            break

        page += 1
        time.sleep(1)          # be polite to Reddit's rate-limiter

    return all_items
