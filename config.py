# ==============================================
# config.py — Toutes les constantes du projet
# ==============================================

# --- Google Cloud / BigQuery ---
KEY_PATH = "caa-assignment-2905cd7ac69b.json"
PROJECT_ID = "caa-assignment"
DATASET = "movies_db"
MOVIES_TABLE = f"{PROJECT_ID}.{DATASET}.movies"
RATINGS_TABLE = f"{PROJECT_ID}.{DATASET}.ratings"

# --- TMDB API ---
TMDB_API_KEY = "a96369e7fd95397bd0a4caff667e46c3"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_TIMEOUT = 5

# --- Limites SQL ---
SEARCH_LIMIT = 20
FILTER_LIMIT = 50
TOP10_LIMIT  = 10

# Bornes de plage pour les filtres de l’interface
MIN_YEAR = 1900
MAX_YEAR = 2024

# Genres exclus des filtres (non pertinents pour la recherche utilisateur)
GENRES_BLACKLIST: set[str] = {"(no genres listed)", "IMAX"}

# Mapping code ISO → nom en français (utilisé dans format_language_label)
LANGUAGE_DISPLAY_MAP: dict[str, str] = {
    # ── Langues majeures ───────────────────────────────────────────────────
    "en": "Anglais",
    "fr": "Français",
    "de": "Allemand",
    "es": "Espagnol",
    "it": "Italien",
    "pt": "Portugais",
    "ru": "Russe",
    "zh": "Chinois (mandarin)",
    "cn": "Chinois (cantonais)",
    "ja": "Japonais",
    "ko": "Coréen",
    "ar": "Arabe",
    "hi": "Hindi",
    # ── Europe ─────────────────────────────────────────────────────────────
    "bg": "Bulgare",
    "bs": "Bosnien",
    "ca": "Catalan",
    "cs": "Tchèque",
    "cy": "Gallois",
    "da": "Danois",
    "el": "Grec",
    "et": "Estonien",
    "eu": "Basque",
    "fi": "Finnois",
    "fy": "Frison occidental",
    "gl": "Galicien",
    "hr": "Croate",
    "hu": "Hongrois",
    "hy": "Arménien",
    "is": "Islandais",
    "lt": "Lituanien",
    "lv": "Letton",
    "mk": "Macédonien",
    "nb": "Norvégien (Bokmål)",
    "nl": "Néerlandais",
    "no": "Norvégien",
    "pl": "Polonais",
    "ro": "Roumain",
    "sc": "Sarde",
    "se": "Same du Nord",
    "sh": "Serbo-croate",
    "sk": "Slovaque",
    "sl": "Slovène",
    "sq": "Albanais",
    "sr": "Serbe",
    "sv": "Suédois",
    "tr": "Turc",
    "uk": "Ukrainien",
    # ── Asie du Sud et du Sud-Est ──────────────────────────────────────────
    "bn": "Bengali",
    "id": "Indonésien",
    "jv": "Javanais",
    "kk": "Kazakh",
    "lo": "Laotien",
    "ml": "Malayâlam",
    "mn": "Mongol",
    "mr": "Marathi",
    "ms": "Malais",
    "ne": "Népalais",
    "ta": "Tamoul",
    "te": "Télougou",
    "tg": "Tadjik",
    "th": "Thaï",
    "tl": "Tagalog",
    "ur": "Ourdou",
    "uz": "Ouzbek",
    "vi": "Vietnamien",
    # ── Moyen-Orient et Asie Centrale ─────────────────────────────────────
    "fa": "Persan",
    "he": "Hébreu",
    "ka": "Géorgien",
    "ku": "Kurde",
    "ps": "Pachto",
    # ── Afrique ────────────────────────────────────────────────────────────
    "am": "Amharique",
    "bm": "Bambara",
    "ff": "Peul",
    "ln": "Lingala",
    "rw": "Kinyarwanda",
    "tn": "Tswana",
    "wo": "Wolof",
    "zu": "Zoulou",
    # ── Langues classiques / rares / codées ───────────────────────────────
    "ay": "Aymara",
    "bo": "Tibétain",
    "dz": "Dzongkha",
    "eo": "Espéranto",
    "iu": "Inuktitut",
    "la": "Latin",
    "qu": "Quechua",
    "xx": "Langue non précisée",
}


def format_language_label(code: str) -> str:
    """
    Retourne le libellé d'affichage d'une langue à partir de son code ISO.

    - Langue connue   → nom français complet  (ex: "Allemand")
    - Langue inconnue → code entre crochets   (ex: "[ab]")
    - Code vide/nul   → chaîne vide

    Utilisé dans format_func des st.multiselect partout dans l'app.
    """
    if not code or not str(code).strip():
        return ""
    code = str(code).strip().lower()
    return LANGUAGE_DISPLAY_MAP.get(code, f"[{code}]")

# --- Messages Utilisateur (UX) ---
MSG_LOADING_TOP10  = "Chargement du Top 10 en cours…"
MSG_SEARCHING      = "Recherche des films en cours…"
MSG_SORTING        = "Application du tri…"
MSG_LOADING_MORE   = "Chargement des résultats supplémentaires…"
MSG_LOADING_DETAIL = "Ouverture de la fiche du film…"

# --- Filtres inline (Sliders de l'interface) ---
# Limites pour les filtres Streamlit
MIN_YEAR_BOUND = 1900
MAX_YEAR_BOUND = 2026
MIN_RATING_BOUND = 0.0
MAX_RATING_BOUND = 5.0


# Options de tri : clé = libellé UI, valeur = sort_by passé à bigquery_client
SORT_OPTIONS: dict = {
    "⭐ Mieux notés → moins bien notés": "rating_desc",
    "⭐ Moins bien notés → mieux notés": "rating_asc",
    "📅 Plus récents → plus anciens":    "year_desc",
    "📅 Plus anciens → plus récents":    "year_asc",
}
