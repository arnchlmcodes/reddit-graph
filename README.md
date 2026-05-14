# Reddit Profile Graph Visualizer

An interactive network graph that maps any Reddit user's public activity (posts, comments, and subreddit participation) into a beautiful, explorable visualization — right in your browser.

**100% client-side.** No backend scraping. No API. No login required. Just pure static HTML you can open directly in your browser.

---

## Features

- **Interactive Graph** — Zoom, pan, drag nodes, and click to open any post/comment on Reddit
- **Grouped Categories** — Subreddits are auto-classified into topic categories (Gaming, Tech, News, etc.) shown as diamond nodes
- **Smart Layout** — Force-directed physics settles into a readable layout, then lets you freely rearrange
- **Rich Tooltips** — Hover any node to see full details: score, date, flair, body preview, and direct links
- **Visual Encoding**
  - Node **size** scales logarithmically with score
  - **Category diamonds** are colour-coded by topic (16 distinct colours)
  - Subreddit labels show **activity count** at a glance
  - Edge **thickness** reflects interaction volume
- **Zero Server Cost** — Everything runs in the browser via JSONP (bypasses CORS naturally). No backend proxy needed!

---

## Quick Start

You don't even need a server to run this!

1. Clone or download this repository.
2. Double-click `index.html` to open it in your browser.
3. Enter a Reddit username.

If you want to host it online, you can simply drop these files into GitHub Pages, Netlify, Cloudflare Pages, or Vercel. It is 100% static!

---

## How It Works

```
  Browser                           Reddit
  ──────                           ──────
  1. User enters username
  2. JS injects <script>   ────→  reddit.com/user/X.json?jsonp=...
  3. JSONP script loads    ←────  (Bypasses CORS naturally)
  4. Browser classifies subreddits into categories
  5. Browser builds vis.js graph
  6. Interactive visualization rendered
```

**Architecture:** User → Category → Subreddit → Post/Comment (4-tier hierarchy)

- All scraping and graph logic happens **entirely in the browser** using a clever JSONP trick to bypass Reddit's CORS policy.
- Reddit traffic comes from users' own browsers — no single IP to throttle!

---

## Project Structure

```
reddit-graph/
├── index.html               # Main page (landing + graph screens)
├── css/
│   └── style.css            # Dark theme, glassmorphism, animations
├── js/
│   ├── app.js               # UI controller & screen transitions
│   ├── scraper.js           # Reddit JSONP fetcher with pagination
│   ├── categories.js        # Subreddit → category classifier (150+ known)
│   └── graph.js             # vis.js network builder
├── .gitignore
├── LICENSE
└── README.md
```

---

## Configuration

| File | What to change | Purpose |
|------|---------------|---------|
| `js/graph.js` | `COLORS` object | Node colours for each type |
| `js/graph.js` | `GRAPH_OPTIONS` object | vis.js physics, spacing, interaction |
| `js/categories.js` | `KNOWN` object | Add subreddit → category mappings |
| `js/categories.js` | `KEYWORD_RULES` array | Fallback keyword patterns |
| `js/categories.js` | `CATEGORY_COLORS` object | Colour for each of the 16 categories |

---

## Limitations

- Reddit's public JSON API returns a **maximum of ~1,000 items** per user (hard Reddit limit)
- **No authentication** — private/quarantined subreddits and removed content won't appear
- Heavy users may take 30–60 seconds to fully paginate (1s delay between pages to respect rate limits)
- **CORS Bypassed:** Uses Reddit's built-in JSONP support so your browser can scrape directly without any API proxies.

---

## License

[MIT](LICENSE)
