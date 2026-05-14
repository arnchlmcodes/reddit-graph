#  Reddit Profile Graph Visualizer

An interactive network graph that maps any Reddit user's public activity (posts, comments, and subreddit participation) into a beautiful, explorable visualization you can open in your browser.

---

##  Features

- **Interactive Graph** — Zoom, pan, drag nodes, and click to open any post/comment on Reddit.
- **Smart Layout** — Force-directed physics (ForceAtlas2) keeps related nodes clustered naturally.
- **Rich Tooltips** — Hover over any node to see full details: score, date, flair, body preview, and direct links.
- **Visual Encoding**
  - Node **size** scales logarithmically with score.
  - Node **colour** encodes type (post / comment / controversial).
  - Edge **thickness** reflects how active a user is in each subreddit.


---

## Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/<your-username>/reddit-graph.git
cd reddit-graph

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

You'll be prompted for a Reddit username. The script will:

1. Fetch all available public activity (paginated, rate-limited).
2. Build an interactive vis.js network graph.
3. Save `<username>_graph.html` and open it in your default browser.

---

##  Project Structure

```
reddit-graph/
├── main.py                    # CLI entry-point
├── reddit_graph/              # Core package
│   ├── __init__.py            # Package metadata & version
│   ├── config.py              # Colour palette & vis.js physics options
│   ├── graph.py               # Graph construction & HTML export
│   ├── scraper.py             # Reddit JSON API fetcher
│   ├── templates.py           # Injected HTML legend & JS click handler
│   └── utils.py               # Shared helpers (clamp, truncate, etc.)
├── requirements.txt           # Python dependencies
├── .gitignore
├── LICENSE                    # MIT
└── README.md
```

---

##  How It Works

```
┌──────────┐     JSON API      ┌───────────┐     pyvis      ┌───────────┐
│  Reddit   │ ──────────────▶  │  Scraper   │ ────────────▶  │  Graph    │
│  (public) │   paginated      │  scraper.py│   items list   │  graph.py │
└──────────┘                   └───────────┘                 └─────┬─────┘
                                                                   │
                                                          HTML + legend + JS
                                                                   │
                                                                   ▼
                                                          username_graph.html
                                                          (open in browser)
```

1. **Scraper** pages through `/user/{name}.json`, normalises each post (`t3`) and comment (`t1`) into a flat dict.
2. **Graph Builder** creates a pyvis `Network` with three tiers of nodes (user → subreddit → activity) and styled edges.
3. **HTML Writer** generates the page, injects the interactive legend and click-to-open handler, and writes UTF-8.

---

##  Configuration

All tunables live in [`reddit_graph/config.py`](reddit_graph/config.py):

| Constant | Purpose |
|----------|---------|
| `COLORS` | Hex colour map for each node type |
| `GRAPH_OPTIONS` | vis.js physics solver, stabilisation, and interaction settings |

To tweak the physics (e.g. make the graph tighter or looser), edit the `forceAtlas2Based` values in `GRAPH_OPTIONS`.

---

##  Limitations

- Reddit's public JSON API returns a **maximum of ~1 000 items** per user (hard limit on their side).
- **No authentication** — private/quarantined subreddits and removed content won't appear.
- Heavy users may take 30-60 seconds to fully paginate due to the 1-second rate-limit delay between pages.
