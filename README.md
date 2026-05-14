#  Reddit Profile Graph Visualizer

An interactive network graph that maps any Reddit user's public activity (posts, comments, and subreddit participation) into a beautiful, explorable visualization you can open in your browser.

---

##  Features

- **Interactive Graph** — Zoom, pan, drag nodes, and click to open any post/comment on Reddit.
- **Grouped Categories** — Subreddits are auto-classified into topic categories (Gaming, Tech, News, etc.) and clustered as diamond nodes in the graph.
- **Smart Layout** — Force-directed physics (ForceAtlas2) keeps related nodes clustered naturally.
- **Rich Tooltips** — Hover over any node to see full details: score, date, flair, body preview, and direct links.
- **Visual Encoding**
  - Node **size** scales logarithmically with score.
  - Node **colour** encodes type (post / comment / controversial).
  - **Category diamonds** are colour-coded by topic (16 distinct colours).
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
│   ├── categories.py          # Subreddit → category classifier (150+ known subs)
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
2. **Classifier** maps each subreddit to a high-level category (Gaming, Tech, News, etc.) using a 150+ entry lookup table with keyword fallback.
3. **Graph Builder** creates a pyvis `Network` with four tiers of nodes (**user → category → subreddit → activity**) and colour-coded edges.
4. **HTML Writer** generates the page, injects the interactive legend and click-to-open handler, and writes UTF-8.

---

##  Configuration

All tunables live in [`reddit_graph/config.py`](reddit_graph/config.py):

| File | Constant | Purpose |
|------|----------|---------|
| `config.py` | `COLORS` | Hex colour map for each node type |
| `config.py` | `GRAPH_OPTIONS` | vis.js physics solver, stabilisation, and interaction settings |
| `categories.py` | `CATEGORY_COLORS` | Colour for each of the 16 topic categories |
| `categories.py` | `_KNOWN` | Subreddit → category lookup table (extend to add more) |
| `categories.py` | `_KEYWORD_RULES` | Fallback keyword patterns for unknown subreddits |

To tweak the physics (e.g. make the graph tighter or looser), edit the `forceAtlas2Based` values in `GRAPH_OPTIONS`.

To add new subreddit mappings, add entries to the `_KNOWN` dict in `categories.py`.

---

##  Limitations

- Reddit's public JSON API returns a **maximum of ~1 000 items** per user (hard limit on their side).
- **No authentication** — private/quarantined subreddits and removed content won't appear.
- Heavy users may take 30-60 seconds to fully paginate due to the 1-second rate-limit delay between pages.
