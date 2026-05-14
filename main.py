#!/usr/bin/env python3
"""
Reddit Profile Graph Visualizer — CLI entry-point.

Usage:
    python main.py
"""

import os
import webbrowser

from reddit_graph.scraper import fetch_all_activity
from reddit_graph.graph import build_graph, write_html


def main() -> None:
    username = input("Enter Reddit username: ").strip()
    if not username:
        print("No username provided — exiting.")
        return

    print(f"\nFetching activity for u/{username}...\n")
    items = fetch_all_activity(username)

    if not items:
        print("No activity found or user does not exist.")
        return

    subs = len({i["subreddit"] for i in items})
    print(f"\nBuilding graph — {len(items)} items across {subs} subreddits...")

    net = build_graph(items, username)
    out = f"{username}_graph.html"
    write_html(net, out, username)

    print(f"Saved -> {out}")
    webbrowser.open("file://" + os.path.abspath(out))


if __name__ == "__main__":
    main()