"""
Subreddit → category mapping and auto-classifier.

Categories group subreddits into high-level topics so the graph can cluster
related communities together visually.
"""

# ── known subreddit → category overrides ──────────────────────────────────────
# Only the most common subreddits are listed; the keyword-based fallback
# handles everything else.

_KNOWN: dict[str, str] = {
    # Technology
    "technology": "Technology", "programming": "Technology", "python": "Technology",
    "javascript": "Technology", "webdev": "Technology", "learnprogramming": "Technology",
    "linux": "Technology", "android": "Technology", "apple": "Technology",
    "computers": "Technology", "machinelearning": "Technology", "datascience": "Technology",
    "artificial": "Technology", "coding": "Technology", "cscareerquestions": "Technology",
    "sysadmin": "Technology", "netsec": "Technology", "golang": "Technology",
    "rust": "Technology", "cpp": "Technology", "java": "Technology",
    "reactjs": "Technology", "node": "Technology", "devops": "Technology",
    "hacking": "Technology", "cybersecurity": "Technology",

    # Gaming
    "gaming": "Gaming", "games": "Gaming", "pcgaming": "Gaming",
    "ps4": "Gaming", "ps5": "Gaming", "xboxone": "Gaming",
    "nintendoswitch": "Gaming", "minecraft": "Gaming", "fortnite": "Gaming",
    "leagueoflegends": "Gaming", "valorant": "Gaming", "overwatch": "Gaming",
    "apex": "Gaming", "apexlegends": "Gaming", "dota2": "Gaming",
    "csgo": "Gaming", "counterstrike": "Gaming", "steam": "Gaming",
    "roblox": "Gaming", "genshinimpact": "Gaming", "eldenring": "Gaming",
    "skyrim": "Gaming", "zelda": "Gaming", "pokemon": "Gaming",
    "gtaonline": "Gaming", "rocketleague": "Gaming", "deadbydaylight": "Gaming",
    "gamedev": "Gaming", "indiegaming": "Gaming", "patientgamers": "Gaming",
    "truegaming": "Gaming", "boardgames": "Gaming",

    # News & Politics
    "news": "News & Politics", "worldnews": "News & Politics",
    "politics": "News & Politics", "geopolitics": "News & Politics",
    "conservative": "News & Politics", "liberal": "News & Politics",
    "neutralpolitics": "News & Politics", "politicaldiscussion": "News & Politics",
    "upliftingnews": "News & Politics", "nottheonion": "News & Politics",
    "inthenews": "News & Politics",

    # Entertainment
    "movies": "Entertainment", "television": "Entertainment", "netflix": "Entertainment",
    "marvelstudios": "Entertainment", "dccomics": "Entertainment",
    "anime": "Entertainment", "manga": "Entertainment",
    "starwars": "Entertainment", "harrypotter": "Entertainment",
    "books": "Entertainment", "comics": "Entertainment",
    "horror": "Entertainment", "scifi": "Entertainment",
    "documentaries": "Entertainment", "youtubers": "Entertainment",
    "youtube": "Entertainment", "twitch": "Entertainment",
    "kpop": "Entertainment", "hiphopheads": "Entertainment",

    # Music
    "music": "Music", "listentothis": "Music", "indieheads": "Music",
    "metal": "Music", "rock": "Music", "electronicmusic": "Music",
    "wearethemusicmakers": "Music", "guitar": "Music", "piano": "Music",
    "musicproduction": "Music",

    # Sports
    "sports": "Sports", "nba": "Sports", "nfl": "Sports",
    "soccer": "Sports", "football": "Sports", "baseball": "Sports",
    "hockey": "Sports", "mma": "Sports", "boxing": "Sports",
    "formula1": "Sports", "tennis": "Sports", "golf": "Sports",
    "cricket": "Sports", "cfb": "Sports", "collegebasketball": "Sports",
    "fantasyfootball": "Sports", "running": "Sports", "fitness": "Sports",

    # Science & Education
    "science": "Science & Education", "askscience": "Science & Education",
    "space": "Science & Education", "physics": "Science & Education",
    "biology": "Science & Education", "chemistry": "Science & Education",
    "math": "Science & Education", "astronomy": "Science & Education",
    "explainlikeimfive": "Science & Education", "todayilearned": "Science & Education",
    "educationalgifs": "Science & Education", "lectures": "Science & Education",

    # Finance & Business
    "personalfinance": "Finance", "investing": "Finance",
    "wallstreetbets": "Finance", "stocks": "Finance",
    "cryptocurrency": "Finance", "bitcoin": "Finance",
    "ethereum": "Finance", "financialindependence": "Finance",
    "realestate": "Finance", "smallbusiness": "Finance",
    "entrepreneur": "Finance",

    # Art & Creative
    "art": "Art & Creative", "drawing": "Art & Creative",
    "photography": "Art & Creative", "photoshopbattles": "Art & Creative",
    "design": "Art & Creative", "graphic_design": "Art & Creative",
    "digitalart": "Art & Creative", "painting": "Art & Creative",
    "crafts": "Art & Creative", "diy": "Art & Creative",
    "woodworking": "Art & Creative", "crochet": "Art & Creative",
    "crossstitch": "Art & Creative",

    # Lifestyle & Health
    "fitness": "Lifestyle & Health", "loseit": "Lifestyle & Health",
    "nutrition": "Lifestyle & Health", "meditation": "Lifestyle & Health",
    "yoga": "Lifestyle & Health", "mentalhealth": "Lifestyle & Health",
    "anxiety": "Lifestyle & Health", "depression": "Lifestyle & Health",
    "selfimprovement": "Lifestyle & Health", "getmotivated": "Lifestyle & Health",
    "skincareaddiction": "Lifestyle & Health", "fashion": "Lifestyle & Health",
    "malefashionadvice": "Lifestyle & Health", "frugal": "Lifestyle & Health",

    # Food & Cooking
    "food": "Food & Cooking", "cooking": "Food & Cooking",
    "recipes": "Food & Cooking", "mealprepsunday": "Food & Cooking",
    "foodporn": "Food & Cooking", "askculinary": "Food & Cooking",
    "baking": "Food & Cooking", "grilling": "Food & Cooking",
    "cocktails": "Food & Cooking", "coffee": "Food & Cooking",
    "beer": "Food & Cooking", "wine": "Food & Cooking",
    "vegan": "Food & Cooking", "vegetarian": "Food & Cooking",

    # Humor & Memes
    "funny": "Humor & Memes", "memes": "Humor & Memes",
    "dankmemes": "Humor & Memes", "me_irl": "Humor & Memes",
    "comedyheaven": "Humor & Memes", "jokes": "Humor & Memes",
    "shitposting": "Humor & Memes", "okbuddyretard": "Humor & Memes",
    "cursedcomments": "Humor & Memes", "holup": "Humor & Memes",
    "tihi": "Humor & Memes", "blursedimages": "Humor & Memes",

    # Discussion & Social
    "askreddit": "Discussion", "casualconversation": "Discussion",
    "unpopularopinion": "Discussion", "changemyview": "Discussion",
    "amitheasshole": "Discussion", "relationship_advice": "Discussion",
    "relationships": "Discussion", "advice": "Discussion",
    "nostupidquestions": "Discussion", "outoftheloop": "Discussion",
    "tooafraidtoask": "Discussion", "trueoffmychest": "Discussion",
    "offmychest": "Discussion", "confessions": "Discussion",
    "tifu": "Discussion", "ama": "Discussion", "iama": "Discussion",

    # Nature & Animals
    "aww": "Nature & Animals", "eyebleach": "Nature & Animals",
    "natureismetal": "Nature & Animals", "natureisfuckinglit": "Nature & Animals",
    "animalsbeingbros": "Nature & Animals", "animalsbeingderps": "Nature & Animals",
    "cats": "Nature & Animals", "dogs": "Nature & Animals",
    "rarepuppers": "Nature & Animals", "aquariums": "Nature & Animals",
    "gardening": "Nature & Animals", "earthporn": "Nature & Animals",
    "camping": "Nature & Animals", "hiking": "Nature & Animals",

    # Geography & Travel
    "travel": "Travel", "backpacking": "Travel",
    "solotravel": "Travel", "digitalnomad": "Travel",
    "roadtrip": "Travel", "cityporn": "Travel",
    "mapporn": "Travel", "geography": "Travel",
}

# ── keyword-based fallback classifier ─────────────────────────────────────────

_KEYWORD_RULES: list[tuple[list[str], str]] = [
    (["game", "gaming", "gamer", "play", "esport", "rpg", "mmo"], "Gaming"),
    (["prog", "code", "dev", "hack", "cyber", "tech", "software", "comput"], "Technology"),
    (["politic", "news", "govern", "elect", "democrat", "republican"], "News & Politics"),
    (["movie", "tv", "show", "film", "anime", "manga", "netflix", "stream"], "Entertainment"),
    (["music", "band", "song", "album", "guitar", "hip hop", "rap"], "Music"),
    (["sport", "nba", "nfl", "soccer", "football", "baseball", "tennis"], "Sports"),
    (["science", "physics", "bio", "chem", "math", "space", "astro"], "Science & Education"),
    (["stock", "crypto", "invest", "financ", "money", "trad"], "Finance"),
    (["art", "draw", "paint", "photo", "design", "craft", "diy"], "Art & Creative"),
    (["food", "cook", "recipe", "bak", "eat", "meal", "kitchen"], "Food & Cooking"),
    (["meme", "funny", "joke", "humor", "lol", "shitpost"], "Humor & Memes"),
    (["fit", "health", "gym", "workout", "diet", "mental", "meditat"], "Lifestyle & Health"),
    (["cat", "dog", "pet", "animal", "nature", "wild", "garden"], "Nature & Animals"),
    (["travel", "trip", "country", "city", "backpack"], "Travel"),
    (["ask", "advice", "opinion", "discuss", "rant", "vent"], "Discussion"),
]


# ── category colours ──────────────────────────────────────────────────────────

CATEGORY_COLORS: dict[str, str] = {
    "Technology":         "#00BCD4",   # Cyan
    "Gaming":             "#9C27B0",   # Purple
    "News & Politics":    "#F44336",   # Red
    "Entertainment":      "#E91E63",   # Pink
    "Music":              "#FF9800",   # Orange
    "Sports":             "#4CAF50",   # Green
    "Science & Education":"#2196F3",   # Blue
    "Finance":            "#FFC107",   # Gold
    "Art & Creative":     "#FF5722",   # Deep orange
    "Food & Cooking":     "#8BC34A",   # Light green
    "Humor & Memes":      "#FFEB3B",   # Yellow
    "Lifestyle & Health": "#009688",   # Teal
    "Nature & Animals":   "#66BB6A",   # Soft green
    "Travel":             "#26C6DA",   # Light cyan
    "Discussion":         "#7E57C2",   # Deep purple
    "Other":              "#78909C",   # Blue-grey
}


def classify_subreddit(name: str) -> str:
    """
    Return the category string for a subreddit name.

    Lookup order:
    1. Exact match in the known-subreddits table (case-insensitive).
    2. Keyword substring match against the subreddit name.
    3. Falls back to ``"Other"``.
    """
    lower = name.lower()

    # 1. exact lookup
    if lower in _KNOWN:
        return _KNOWN[lower]

    # 2. keyword heuristic
    for keywords, category in _KEYWORD_RULES:
        if any(kw in lower for kw in keywords):
            return category

    return "Other"
