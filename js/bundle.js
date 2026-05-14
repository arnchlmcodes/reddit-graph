/**
 * Subreddit → category classifier.
 * Ports the Python categories.py to JavaScript.
 */

// ── Known subreddit → category overrides ──────────────────────────
const KNOWN = {
  // Technology
  technology: "Technology", programming: "Technology", python: "Technology",
  javascript: "Technology", webdev: "Technology", learnprogramming: "Technology",
  linux: "Technology", android: "Technology", apple: "Technology",
  computers: "Technology", machinelearning: "Technology", datascience: "Technology",
  coding: "Technology", cscareerquestions: "Technology", sysadmin: "Technology",
  netsec: "Technology", golang: "Technology", rust: "Technology",
  cpp: "Technology", java: "Technology", reactjs: "Technology",
  node: "Technology", devops: "Technology", hacking: "Technology",
  cybersecurity: "Technology",

  // Gaming
  gaming: "Gaming", games: "Gaming", pcgaming: "Gaming",
  ps4: "Gaming", ps5: "Gaming", xboxone: "Gaming",
  nintendoswitch: "Gaming", minecraft: "Gaming", fortnite: "Gaming",
  leagueoflegends: "Gaming", valorant: "Gaming", overwatch: "Gaming",
  apex: "Gaming", apexlegends: "Gaming", dota2: "Gaming",
  csgo: "Gaming", counterstrike: "Gaming", steam: "Gaming",
  roblox: "Gaming", genshinimpact: "Gaming", eldenring: "Gaming",
  skyrim: "Gaming", zelda: "Gaming", pokemon: "Gaming",
  gtaonline: "Gaming", rocketleague: "Gaming", deadbydaylight: "Gaming",
  gamedev: "Gaming", indiegaming: "Gaming", patientgamers: "Gaming",
  truegaming: "Gaming", boardgames: "Gaming",

  // News & Politics
  news: "News & Politics", worldnews: "News & Politics",
  politics: "News & Politics", geopolitics: "News & Politics",
  conservative: "News & Politics", liberal: "News & Politics",
  neutralpolitics: "News & Politics", politicaldiscussion: "News & Politics",
  upliftingnews: "News & Politics", nottheonion: "News & Politics",
  inthenews: "News & Politics",

  // Entertainment
  movies: "Entertainment", television: "Entertainment", netflix: "Entertainment",
  marvelstudios: "Entertainment", dccomics: "Entertainment",
  anime: "Entertainment", manga: "Entertainment",
  starwars: "Entertainment", harrypotter: "Entertainment",
  books: "Entertainment", comics: "Entertainment",
  horror: "Entertainment", scifi: "Entertainment",
  documentaries: "Entertainment", youtube: "Entertainment", twitch: "Entertainment",
  kpop: "Entertainment", hiphopheads: "Entertainment",

  // Music
  music: "Music", listentothis: "Music", indieheads: "Music",
  metal: "Music", rock: "Music", electronicmusic: "Music",
  wearethemusicmakers: "Music", guitar: "Music", piano: "Music",
  musicproduction: "Music",

  // Sports
  sports: "Sports", nba: "Sports", nfl: "Sports",
  soccer: "Sports", football: "Sports", baseball: "Sports",
  hockey: "Sports", mma: "Sports", boxing: "Sports",
  formula1: "Sports", tennis: "Sports", golf: "Sports",
  cricket: "Sports", cfb: "Sports", collegebasketball: "Sports",
  fantasyfootball: "Sports", running: "Sports",

  // Science & Education
  science: "Science & Education", askscience: "Science & Education",
  space: "Science & Education", physics: "Science & Education",
  biology: "Science & Education", chemistry: "Science & Education",
  math: "Science & Education", astronomy: "Science & Education",
  explainlikeimfive: "Science & Education", todayilearned: "Science & Education",

  // Finance
  personalfinance: "Finance", investing: "Finance",
  wallstreetbets: "Finance", stocks: "Finance",
  cryptocurrency: "Finance", bitcoin: "Finance",
  ethereum: "Finance", financialindependence: "Finance",
  realestate: "Finance", smallbusiness: "Finance", entrepreneur: "Finance",

  // Art & Creative
  art: "Art & Creative", drawing: "Art & Creative",
  photography: "Art & Creative", photoshopbattles: "Art & Creative",
  design: "Art & Creative", graphic_design: "Art & Creative",
  digitalart: "Art & Creative", painting: "Art & Creative",
  crafts: "Art & Creative", diy: "Art & Creative",
  woodworking: "Art & Creative",

  // Lifestyle & Health
  fitness: "Lifestyle & Health", loseit: "Lifestyle & Health",
  nutrition: "Lifestyle & Health", meditation: "Lifestyle & Health",
  yoga: "Lifestyle & Health", mentalhealth: "Lifestyle & Health",
  anxiety: "Lifestyle & Health", depression: "Lifestyle & Health",
  selfimprovement: "Lifestyle & Health", getmotivated: "Lifestyle & Health",
  skincareaddiction: "Lifestyle & Health", fashion: "Lifestyle & Health",
  malefashionadvice: "Lifestyle & Health",

  // Food & Cooking
  food: "Food & Cooking", cooking: "Food & Cooking",
  recipes: "Food & Cooking", mealprepsunday: "Food & Cooking",
  foodporn: "Food & Cooking", askculinary: "Food & Cooking",
  baking: "Food & Cooking", grilling: "Food & Cooking",
  cocktails: "Food & Cooking", coffee: "Food & Cooking",
  beer: "Food & Cooking", wine: "Food & Cooking",
  vegan: "Food & Cooking", vegetarian: "Food & Cooking",

  // Humor & Memes
  funny: "Humor & Memes", memes: "Humor & Memes",
  dankmemes: "Humor & Memes", me_irl: "Humor & Memes",
  comedyheaven: "Humor & Memes", jokes: "Humor & Memes",
  shitposting: "Humor & Memes", cursedcomments: "Humor & Memes",
  holup: "Humor & Memes", tihi: "Humor & Memes", blursedimages: "Humor & Memes",

  // Discussion & Social
  askreddit: "Discussion", casualconversation: "Discussion",
  unpopularopinion: "Discussion", changemyview: "Discussion",
  amitheasshole: "Discussion", relationship_advice: "Discussion",
  relationships: "Discussion", advice: "Discussion",
  nostupidquestions: "Discussion", outoftheloop: "Discussion",
  tooafraidtoask: "Discussion", trueoffmychest: "Discussion",
  offmychest: "Discussion", confessions: "Discussion",
  tifu: "Discussion", iama: "Discussion",

  // Nature & Animals
  aww: "Nature & Animals", eyebleach: "Nature & Animals",
  natureismetal: "Nature & Animals", natureisfuckinglit: "Nature & Animals",
  animalsbeingbros: "Nature & Animals", animalsbeingderps: "Nature & Animals",
  cats: "Nature & Animals", dogs: "Nature & Animals",
  rarepuppers: "Nature & Animals", aquariums: "Nature & Animals",
  gardening: "Nature & Animals", earthporn: "Nature & Animals",
  camping: "Nature & Animals", hiking: "Nature & Animals",

  // Travel
  travel: "Travel", backpacking: "Travel",
  solotravel: "Travel", digitalnomad: "Travel",
  roadtrip: "Travel", cityporn: "Travel",
  mapporn: "Travel", geography: "Travel",
};

// ── Keyword fallback rules ────────────────────────────────────────
const KEYWORD_RULES = [
  [["game", "gaming", "gamer", "play", "esport", "rpg", "mmo"], "Gaming"],
  [["prog", "code", "dev", "hack", "cyber", "tech", "software", "comput"], "Technology"],
  [["politic", "news", "govern", "elect", "democrat", "republican"], "News & Politics"],
  [["movie", "tv", "show", "film", "anime", "manga", "netflix", "stream"], "Entertainment"],
  [["music", "band", "song", "album", "guitar", "hip hop", "rap"], "Music"],
  [["sport", "nba", "nfl", "soccer", "football", "baseball", "tennis"], "Sports"],
  [["science", "physics", "bio", "chem", "math", "space", "astro"], "Science & Education"],
  [["stock", "crypto", "invest", "financ", "money", "trad"], "Finance"],
  [["art", "draw", "paint", "photo", "design", "craft", "diy"], "Art & Creative"],
  [["food", "cook", "recipe", "bak", "eat", "meal", "kitchen"], "Food & Cooking"],
  [["meme", "funny", "joke", "humor", "lol", "shitpost"], "Humor & Memes"],
  [["fit", "health", "gym", "workout", "diet", "mental", "meditat"], "Lifestyle & Health"],
  [["cat", "dog", "pet", "animal", "nature", "wild", "garden"], "Nature & Animals"],
  [["travel", "trip", "country", "city", "backpack"], "Travel"],
  [["ask", "advice", "opinion", "discuss", "rant", "vent"], "Discussion"],
];

// ── Category colours ──────────────────────────────────────────────
const CATEGORY_COLORS = {
  "Technology":          "#00BCD4",
  "Gaming":              "#9C27B0",
  "News & Politics":     "#F44336",
  "Entertainment":       "#E91E63",
  "Music":               "#FF9800",
  "Sports":              "#4CAF50",
  "Science & Education": "#2196F3",
  "Finance":             "#FFC107",
  "Art & Creative":      "#FF5722",
  "Food & Cooking":      "#8BC34A",
  "Humor & Memes":       "#FFEB3B",
  "Lifestyle & Health":  "#009688",
  "Nature & Animals":    "#66BB6A",
  "Travel":              "#26C6DA",
  "Discussion":          "#7E57C2",
  "Other":               "#78909C",
};

/**
 * Classify a subreddit name into a category.
 * @param {string} name — subreddit name (without r/)
 * @returns {string} category label
 */
function classifySubreddit(name) {
  const lower = name.toLowerCase();

  // 1. exact lookup
  if (KNOWN[lower]) return KNOWN[lower];

  // 2. keyword heuristic
  for (const [keywords, category] of KEYWORD_RULES) {
    if (keywords.some(kw => lower.includes(kw))) return category;
  }

  return "Other";
}


/**
 * Reddit JSONP scraper — fetches user activity from the browser directly.
 * Uses JSONP to bypass CORS restrictions entirely! Zero backend needed.
 */

const PAGE_SIZE = 25;

/**
 * Convert UNIX epoch to YYYY-MM-DD string.
 */
function ts(epoch) {
  return new Date(epoch * 1000).toISOString().slice(0, 10);
}

/**
 * Parse a t1 (comment) child.
 */
function parseComment(d) {
  return {
    type: "comment",
    id: d.id,
    subreddit: d.subreddit,
    created: ts(d.created_utc),
    score: d.score,
    controversial: d.controversiality === 1,
    isOwnPost: d.is_submitter,
    edited: d.edited !== false,
    body: (d.body || "").trim(),
    postTitle: d.link_title || "",
    permalink: "https://reddit.com" + d.permalink,
  };
}

/**
 * Parse a t3 (post) child.
 */
function parsePost(d) {
  return {
    type: "post",
    id: d.id,
    subreddit: d.subreddit,
    created: ts(d.created_utc),
    title: d.title || "",
    body: (d.selftext || "").trim(),
    score: d.score,
    upvoteRatio: d.upvote_ratio || 0,
    numComments: d.num_comments,
    flair: d.link_flair_text || "",
    edited: d.edited !== false,
    permalink: "https://reddit.com" + d.permalink,
  };
}

let jsonpCounter = 0;

/**
 * Fetch one page of user activity JSON via JSONP.
 * This completely bypasses CORS restrictions directly in the browser.
 */
function fetchPageJSONP(username, after = "") {
  return new Promise((resolve, reject) => {
    const callbackName = `reddit_jsonp_${Date.now()}_${jsonpCounter++}`;
    const url = `https://www.reddit.com/user/${encodeURIComponent(username)}.json?limit=${PAGE_SIZE}&after=${encodeURIComponent(after)}&jsonp=${callbackName}`;
    
    const script = document.createElement("script");
    script.src = url;
    
    // Cleanup function
    const cleanup = () => {
      delete window[callbackName];
      if (script.parentNode) script.parentNode.removeChild(script);
    };

    window[callbackName] = (data) => {
      cleanup();
      
      if (data.error) {
        reject(new Error(data.message || "Reddit API error"));
        return;
      }
      resolve(data);
    };

    script.onerror = () => {
      cleanup();
      // If the user doesn't exist or profile is private, Reddit returns an HTML error page, 
      // which fails to parse as a script and triggers this onerror handler.
      reject(new Error("Could not reach Reddit. The user may not exist, their profile might be private/suspended, or you are rate-limited."));
    };

    document.head.appendChild(script);
    
    // Fallback timeout just in case it hangs forever
    setTimeout(() => {
      cleanup();
      reject(new Error("Reddit request timed out."));
    }, 15000);
  });
}

/**
 * Fetch all activity for a user, paginating through all available pages.
 * @param {string} username
 * @param {function} onProgress — called with (page, itemsSoFar)
 * @returns {Promise<Array>} — array of normalised activity items
 */
async function fetchAllActivity(username, onProgress = () => {}) {
  const allItems = [];
  const seenIds = new Set();
  let after = "";
  let page = 1;

  while (true) {
    onProgress(page, allItems.length);

    const data = await fetchPageJSONP(username, after);
    if (!data || !data.data) break;

    const batch = [];
    for (const child of data.data.children) {
      let item;
      if (child.kind === "t1") item = parseComment(child.data);
      else if (child.kind === "t3") item = parsePost(child.data);

      if (item && !seenIds.has(item.id)) {
        seenIds.add(item.id);
        batch.push(item);
      }
    }

    if (batch.length === 0) break;

    allItems.push(...batch);
    after = data.data.after || "";
    if (!after) break;

    page++;
    
    // Rate-limit: 1.5 seconds between pages to avoid Reddit rate limiting
    await new Promise(r => setTimeout(r, 1500));
  }

  return allItems;
}


/**
 * vis.js graph builder — creates an interactive network from Reddit activity.
 *
 * Graph hierarchy: User ★ → Category ◆ → Subreddit ● → Activity ·
 */


// ── Colour palette (matches CSS vars) ─────────────────────────────
const COLORS = {
  user:      "#FF4500",
  subreddit: "#4FC3F7",
  post:      "#69F0AE",
  comment:   "#FFD54F",
  flagged:   "#FF5252",
};

// ── Helpers ───────────────────────────────────────────────────────

function clamp(val, lo, hi) { return Math.max(lo, Math.min(hi, val)); }

function scoreToSize(score, base = 10, scale = 20, cap = 40) {
  if (score <= 0) return base;
  return clamp(base + Math.round(Math.log1p(score) * scale / Math.log1p(100)), base, cap);
}

function truncate(text, n = 300) {
  if (!text) return "";
  return text.length <= n ? text : text.slice(0, n) + "...";
}

// ── Graph options ─────────────────────────────────────────────────
const GRAPH_OPTIONS = {
  physics: {
    enabled: true,
    forceAtlas2Based: {
      gravitationalConstant: -120,
      centralGravity: 0.008,
      springLength: 200,
      springConstant: 0.05,
      damping: 0.45,
      avoidOverlap: 0.6,
    },
    solver: "forceAtlas2Based",
    stabilization: { iterations: 250 },
    maxVelocity: 50,
    minVelocity: 0.75,
  },
  interaction: {
    hover: true,
    tooltipDelay: 100,
    navigationButtons: true,
    keyboard: true,
    zoomSpeed: 0.6,
  },
  edges: {
    smooth: { type: "continuous" },
    arrows: { to: { enabled: true, scaleFactor: 0.4 } },
  },
};

// ── Main builder ──────────────────────────────────────────────────

/**
 * Build and render a vis.js Network inside the given container.
 * @param {HTMLElement} container
 * @param {Array} items — normalised activity list
 * @param {string} username
 * @returns {{ network, stats }} — the vis Network instance + computed stats
 */
function buildGraph(container, items, username) {
  const nodes = new vis.DataSet();
  const edges = new vis.DataSet();

  // Classify subreddits
  const subToCat = {};
  for (const item of items) {
    if (!subToCat[item.subreddit]) {
      subToCat[item.subreddit] = classifySubreddit(item.subreddit);
    }
  }

  // 1. User node
  nodes.add({
    id: `user:${username}`,
    label: `u/${username}`,
    title: `<b>u/${username}</b><br>${items.length} total activities`,
    color: COLORS.user,
    size: 65,
    shape: "star",
    font: { size: 24, color: "#ffffff", bold: true, strokeWidth: 4, strokeColor: "#000" },
  });

  // 2. Category nodes
  const catStats = {};
  for (const item of items) {
    const cat = subToCat[item.subreddit];
    if (!catStats[cat]) catStats[cat] = { count: 0, subs: new Set() };
    catStats[cat].count++;
    catStats[cat].subs.add(item.subreddit);
  }

  for (const [cat, stats] of Object.entries(catStats)) {
    const colour = CATEGORY_COLORS[cat] || CATEGORY_COLORS["Other"];
    const numSubs = stats.subs.size;

    nodes.add({
      id: `cat:${cat}`,
      label: `${cat.toUpperCase()} (${numSubs})`,
      title: `<b>${cat}</b><br>${stats.count} activities across ${numSubs} subreddit${numSubs !== 1 ? "s" : ""}`,
      color: { background: colour, border: "#ffffff", highlight: { background: colour, border: "#ffffff" } },
      size: clamp(30 + stats.count * 2, 30, 70),
      shape: "diamond",
      borderWidth: 2,
      font: { size: 18, color: "#ffffff", bold: true, strokeWidth: 4, strokeColor: "#000" },
    });
    edges.add({
      from: `user:${username}`,
      to: `cat:${cat}`,
      width: clamp(2 + stats.count * 0.4, 2, 10),
      color: { color: colour + "55", highlight: colour },
      title: `${stats.count} activities`,
    });
  }

  // 3. Subreddit nodes
  const subItems = {};
  for (const item of items) {
    (subItems[item.subreddit] ||= []).push(item);
  }

  for (const [sub, subList] of Object.entries(subItems)) {
    const cat = subToCat[sub];
    const catColour = CATEGORY_COLORS[cat] || CATEGORY_COLORS["Other"];
    const count = subList.length;
    const posts = subList.filter(i => i.type === "post").length;
    const comments = subList.filter(i => i.type === "comment").length;

    nodes.add({
      id: `sub:${sub}`,
      label: `r/${sub} · ${count}`,
      title: `<b>r/${sub}</b><br>Category: ${cat}<br>${count} activities<br>${posts} posts, ${comments} comments<br><a href="https://reddit.com/r/${sub}" target="_blank">open subreddit</a>`,
      color: { background: COLORS.subreddit, border: catColour, highlight: { background: "#81D4FA", border: catColour } },
      size: clamp(20 + count * 5, 20, 65),
      shape: "dot",
      url: `https://reddit.com/r/${sub}`,
      borderWidth: 3,
      borderWidthSelected: 4,
      font: { size: 15, color: "#E0F7FA", bold: true, strokeWidth: 3, strokeColor: "#000" },
    });
    edges.add({
      from: `cat:${cat}`,
      to: `sub:${sub}`,
      width: clamp(1.5 + count * 0.5, 1.5, 7),
      color: { color: catColour + "33", highlight: catColour },
      title: `${count} interactions`,
    });
  }

  // 4. Activity nodes (posts & comments)
  for (const item of items) {
    const nodeId = `${item.type}:${item.id}`;
    const flags = [];
    if (item.controversial) flags.push("CONTROVERSIAL");
    if (item.edited) flags.push("EDITED");
    if (item.isOwnPost) flags.push("OWN POST");
    const flagHtml = flags.length
      ? `<br><b style="color:#ff6b6b">${flags.join(" | ")}</b>`
      : "";

    const color = item.controversial ? COLORS.flagged : COLORS[item.type];

    let tooltip;
    let nodeLabel;
    if (item.type === "post") {
      const ratio = Math.round((item.upvoteRatio || 0) * 100);
      const body = item.body ? truncate(item.body) : "(link post)";
      tooltip =
        `<b>[POST] ${truncate(item.title, 80)}</b>${flagHtml}<br><br>` +
        `r/${item.subreddit} &middot; ${item.created}<br>` +
        `Score: ${item.score} (${ratio}% upvoted) &middot; ${item.numComments} comments<br>` +
        (item.flair ? `Flair: ${item.flair}<br>` : "") +
        `<br>${body}<br><br>` +
        `<a href="${item.permalink}" target="_blank">open post</a>`;
      nodeLabel = truncate(item.title, 25);
    } else {
      tooltip =
        `<b>[COMMENT]</b>${flagHtml}<br><br>` +
        `r/${item.subreddit} &middot; ${item.created}<br>` +
        `Score: ${item.score}<br>` +
        `On: <i>${truncate(item.postTitle, 80)}</i><br><br>` +
        `${truncate(item.body)}<br><br>` +
        `<a href="${item.permalink}" target="_blank">open comment</a>`;
      nodeLabel = truncate(item.body, 25);
    }

    nodes.add({
      id: nodeId,
      label: nodeLabel,
      title: tooltip,
      color: { background: color + "CC", border: color, highlight: { background: "#ffffff", border: color } },
      size: clamp(scoreToSize(item.score) - 2, 6, 40),
      shape: item.type === "post" ? "box" : "dot",
      font: { size: 11, color: "#bbbbbb" },
      url: item.permalink,
    });
    edges.add({
      from: `sub:${item.subreddit}`,
      to: nodeId,
      color: { color: "#2a2a2a", highlight: "#888" },
      width: 0.5,
    });
  }

  // Build network
  const network = new vis.Network(container, { nodes, edges }, GRAPH_OPTIONS);

  // Click to open Reddit URL
  network.on("click", (params) => {
    if (params.nodes.length > 0) {
      const nodeData = nodes.get(params.nodes[0]);
      if (nodeData && nodeData.url) {
        window.open(nodeData.url, "_blank");
      }
    }
  });

  // Stats
  const stats = {
    totalItems: items.length,
    totalSubs: Object.keys(subItems).length,
    totalCats: Object.keys(catStats).length,
  };

  return { network, stats };
}


/**
 * App controller — wires up the UI to the scraper and graph builder.
 */


// ── DOM refs ──────────────────────────────────────────────────────
const landing      = document.getElementById("landing");
const loadingEl    = document.getElementById("loading");
const loadingStatus= document.getElementById("loadingStatus");
const progressFill = document.getElementById("progressFill");
const graphScreen  = document.getElementById("graphScreen");
const graphContainer = document.getElementById("graphContainer");
const form         = document.getElementById("usernameForm");
const input        = document.getElementById("usernameInput");
const submitBtn    = document.getElementById("submitBtn");
const errorMsg     = document.getElementById("errorMsg");
const backBtn      = document.getElementById("backBtn");
const statUser     = document.getElementById("statUser");
const statItems    = document.getElementById("statItems");
const statSubs     = document.getElementById("statSubs");
const statCats     = document.getElementById("statCats");

let currentNetwork = null;

// ── Screen transitions ────────────────────────────────────────────
function showScreen(screen) {
  landing.hidden     = screen !== "landing";
  loadingEl.hidden   = screen !== "loading";
  graphScreen.hidden = screen !== "graph";

  if (screen === "landing") {
    landing.classList.remove("fade-out");
  }
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.hidden = false;
}

function clearError() {
  errorMsg.hidden = true;
}

// ── Main flow ─────────────────────────────────────────────────────
async function visualize(username) {
  clearError();
  submitBtn.disabled = true;

  // Transition to loading
  landing.classList.add("fade-out");
  await new Promise(r => setTimeout(r, 400));
  showScreen("loading");
  loadingStatus.textContent = "Connecting to Reddit...";
  progressFill.style.width = "5%";

  try {
    // Fetch activity with progress updates
    const items = await fetchAllActivity(username, (page, count) => {
      loadingStatus.textContent = `Page ${page} — ${count} items found`;
      progressFill.style.width = Math.min(10 + page * 6, 80) + "%";
    });

    if (!items || items.length === 0) {
      throw new Error("No activity found. The user may not exist or has no public posts.");
    }

    // Build graph
    loadingStatus.textContent = `Building graph with ${items.length} items...`;
    progressFill.style.width = "90%";
    await new Promise(r => setTimeout(r, 200)); // let UI update

    // Clean up previous network
    if (currentNetwork) {
      currentNetwork.destroy();
      currentNetwork = null;
    }
    graphContainer.innerHTML = "";

    const { network, stats } = buildGraph(graphContainer, items, username);
    currentNetwork = network;

    // Fill stats bar
    statUser.textContent  = `u/${username}`;
    statItems.textContent = `${stats.totalItems} activities`;
    statSubs.textContent  = `${stats.totalSubs} subreddits`;
    statCats.textContent  = `${stats.totalCats} categories`;

    progressFill.style.width = "100%";
    await new Promise(r => setTimeout(r, 300));

    // Show graph
    showScreen("graph");

  } catch (err) {
    console.error(err);
    showScreen("landing");
    showError(err.message || "Something went wrong. Please try again.");
  } finally {
    submitBtn.disabled = false;
  }
}

// ── Event listeners ───────────────────────────────────────────────
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = input.value.trim();
  if (!username) return;
  visualize(username);
});

backBtn.addEventListener("click", () => {
  showScreen("landing");
  input.focus();
});

// Focus input on load
input.focus();


