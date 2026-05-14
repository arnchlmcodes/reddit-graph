"""
Build a pyvis / vis.js interactive network graph from scraped Reddit activity.

Graph hierarchy:  User → Category → Subreddit → Post/Comment
"""

from pyvis.network import Network

from .categories import CATEGORY_COLORS, classify_subreddit
from .config import COLORS, GRAPH_OPTIONS
from .templates import CLICK_HANDLER_JS, LEGEND_HTML
from .utils import clamp, score_to_size, truncate


# ── graph construction ─────────────────────────────────────────────────────────


def build_graph(items: list[dict], username: str) -> Network:
    """
    Return a fully-populated :class:`~pyvis.network.Network` with:

    * a central **user** star node
    * **category** ring nodes grouping related subreddits
    * one **subreddit** node per unique subreddit
    * one **post** or **comment** node per activity item
    * edges: user → category → subreddit → item
    """
    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#1a1a1b",
        font_color="#d7dadc",
        directed=True,
        cdn_resources="in_line",
    )
    net.set_options(GRAPH_OPTIONS)

    _add_user_node(net, username, len(items))

    # classify every subreddit
    sub_to_cat: dict[str, str] = {}
    for item in items:
        sub = item["subreddit"]
        if sub not in sub_to_cat:
            sub_to_cat[sub] = classify_subreddit(sub)

    _add_category_nodes(net, items, sub_to_cat, username)
    _add_subreddit_nodes(net, items, sub_to_cat)
    _add_activity_nodes(net, items)

    return net


# ── HTML output ────────────────────────────────────────────────────────────────


def write_html(net: Network, path: str, username: str) -> None:
    """Generate the graph HTML, inject legend + click handler, and write as UTF-8."""
    html = net.generate_html(name=path)

    legend = LEGEND_HTML.replace("{USERNAME}", username)
    html = html.replace("</body>", legend + CLICK_HANDLER_JS + "</body>")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


# ── private helpers ────────────────────────────────────────────────────────────


def _add_user_node(net: Network, username: str, total: int) -> None:
    net.add_node(
        f"user:{username}",
        label=f"u/{username}",
        title=f"<b>u/{username}</b><br>{total} total activities",
        color=COLORS["user"],
        size=50,
        shape="star",
        font={"size": 18, "color": "#ffffff"},
    )


def _add_category_nodes(
    net: Network,
    items: list[dict],
    sub_to_cat: dict[str, str],
    username: str,
) -> None:
    """Add one node per category and connect it to the central user node."""
    # gather stats per category
    cat_stats: dict[str, dict] = {}
    for item in items:
        cat = sub_to_cat[item["subreddit"]]
        if cat not in cat_stats:
            cat_stats[cat] = {"count": 0, "subs": set()}
        cat_stats[cat]["count"] += 1
        cat_stats[cat]["subs"].add(item["subreddit"])

    for cat, stats in cat_stats.items():
        cat_id = f"cat:{cat}"
        count = stats["count"]
        num_subs = len(stats["subs"])
        colour = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["Other"])

        net.add_node(
            cat_id,
            label=cat,
            title=(
                f"<b>{cat}</b><br>"
                f"{count} activities across {num_subs} subreddit{'s' if num_subs != 1 else ''}"
            ),
            color={
                "background": colour,
                "border": colour,
                "highlight": {"background": colour, "border": "#ffffff"},
            },
            size=clamp(20 + count * 2, 20, 60),
            shape="diamond",
            font={"size": 14, "color": "#ffffff", "strokeWidth": 3, "strokeColor": "#000000"},
        )
        net.add_edge(
            f"user:{username}",
            cat_id,
            width=clamp(1.5 + count * 0.3, 1.5, 8),
            color={"color": colour + "66", "highlight": colour},
            title=f"{count} activities",
        )


def _add_subreddit_nodes(
    net: Network,
    items: list[dict],
    sub_to_cat: dict[str, str],
) -> None:
    sub_items: dict[str, list] = {}
    for item in items:
        sub_items.setdefault(item["subreddit"], []).append(item)

    for sub, sub_list in sub_items.items():
        sub_id = f"sub:{sub}"
        cat_id = f"cat:{sub_to_cat[sub]}"
        count = len(sub_list)
        posts = sum(1 for i in sub_list if i["type"] == "post")
        comments = sum(1 for i in sub_list if i["type"] == "comment")
        cat_colour = CATEGORY_COLORS.get(sub_to_cat[sub], CATEGORY_COLORS["Other"])

        net.add_node(
            sub_id,
            label=f"r/{sub}",
            title=(
                f"<b>r/{sub}</b><br>"
                f"Category: {sub_to_cat[sub]}<br>"
                f"{count} activities<br>"
                f"{posts} posts, {comments} comments<br>"
                f"<a href='https://reddit.com/r/{sub}' target='_blank'>open subreddit</a>"
            ),
            color=COLORS["subreddit"],
            size=clamp(15 + count * 3, 15, 55),
            shape="dot",
            url=f"https://reddit.com/r/{sub}",
            borderWidth=2,
            borderWidthSelected=3,
        )
        # edge: category → subreddit
        net.add_edge(
            cat_id,
            sub_id,
            width=clamp(1 + count * 0.4, 1, 8),
            color={"color": cat_colour + "44", "highlight": cat_colour},
            title=f"{count} interactions",
        )


def _add_activity_nodes(net: Network, items: list[dict]) -> None:
    for item in items:
        sub_id = f"sub:{item['subreddit']}"
        node_id = f"{item['type']}:{item['id']}"

        flags = []
        if item.get("controversial"):
            flags.append("CONTROVERSIAL")
        if item.get("edited"):
            flags.append("EDITED")
        if item.get("is_own_post"):
            flags.append("OWN POST")
        flag_html = (
            "<br><b style='color:#ff6b6b'>" + " | ".join(flags) + "</b>"
            if flags
            else ""
        )

        color = COLORS["flagged"] if item.get("controversial") else COLORS[item["type"]]

        if item["type"] == "post":
            label, tooltip = _post_tooltip(item, flag_html)
        else:
            label, tooltip = _comment_tooltip(item, flag_html)

        net.add_node(
            node_id,
            label=label,
            title=tooltip,
            color=color,
            size=score_to_size(item["score"]),
            shape="box" if item["type"] == "post" else "ellipse",
            url=item["permalink"],
            font={"size": 9, "color": "#d7dadc"},
        )
        net.add_edge(
            sub_id,
            node_id,
            color={"color": "#444", "highlight": "#888"},
            width=1,
        )


def _post_tooltip(item: dict, flag_html: str) -> tuple[str, str]:
    body_preview = truncate(item["body"]) if item["body"] else "(link post)"
    ratio = int((item.get("upvote_ratio") or 0) * 100)
    tooltip = (
        f"<b>[POST] {truncate(item['title'], 80)}</b>{flag_html}<br><br>"
        f"r/{item['subreddit']} &middot; {item['created']}<br>"
        f"Score: {item['score']} ({ratio}% upvoted) &middot; {item['num_comments']} comments<br>"
        + (f"Flair: {item['flair']}<br>" if item["flair"] else "")
        + f"<br>{body_preview}<br><br>"
        f"<a href='{item['permalink']}' target='_blank'>open post</a>"
    )
    return truncate(item["title"], 35), tooltip


def _comment_tooltip(item: dict, flag_html: str) -> tuple[str, str]:
    tooltip = (
        f"<b>[COMMENT]</b>{flag_html}<br><br>"
        f"r/{item['subreddit']} &middot; {item['created']}<br>"
        f"Score: {item['score']}<br>"
        f"On: <i>{truncate(item['post_title'], 80)}</i><br><br>"
        f"{truncate(item['body'])}<br><br>"
        f"<a href='{item['permalink']}' target='_blank'>open comment</a>"
    )
    return truncate(item["body"], 35), tooltip
