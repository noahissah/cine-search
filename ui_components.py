# ==============================================
# ui_components.py — Composants HTML/CSS purs
# Aucun appel st. ici : chaque fonction
# reçoit des données et retourne une chaîne HTML.
# ==============================================

# Couleurs associées à chaque genre (badges HTML)
GENRE_COLORS: dict[str, str] = {
    "Action":      "#e05c5c",
    "Adventure":   "#d97c3a",
    "Animation":   "#c8951a",
    "Comedy":      "#3a9e6e",
    "Crime":       "#7c5cbf",
    "Documentary": "#1e8a7a",
    "Drama":       "#3580b8",
    "Family":      "#c0607a",
    "Fantasy":     "#5c52c0",
    "Horror":      "#a03030",
    "Music":       "#b8952a",
    "Mystery":     "#607080",
    "Romance":     "#bf5090",
    "Sci-Fi":      "#1a9ea8",
    "Thriller":    "#708090",
    "War":         "#8880c0",
    "Western":     "#b08840",
}


# ── 1. CSS global (thème sombre) ──────────────────────────────────────────────

def get_global_css() -> str:
    """
    Retourne le bloc <style> complet du thème sombre.
    Palette : #0f1117 (fond), #1a1d27/#21252f (surfaces), #38bdf8 (accent teal).
    Injecté une seule fois dans app.py via st.markdown(..., unsafe_allow_html=True).
    """
    return """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0f1117 !important;
    color: #e2e8f0 !important;
}
.stApp { background: #0f1117; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Remove default top padding ── */
.block-container { padding-top: 0 !important; }

/* ── Hero banner ── */
.cine-hero {
    background: linear-gradient(160deg, #0f1117 0%, #141824 60%, #0f1a24 100%);
    border-bottom: 1px solid rgba(56, 189, 248, 0.18);
    text-align: center;
    padding: 2.4rem 1rem 1.8rem;
    margin-bottom: 1.5rem;
}
.cine-hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #f1f5f9;
    margin: 0 0 0.3rem;
}
.cine-hero h1 .accent {
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cine-hero p {
    color: #64748b;
    font-size: 0.9rem;
    margin: 0;
    letter-spacing: 0.3px;
}

/* ── Search bar ── */
.stTextInput input {
    background: #1a1d27 !important;
    border: 1.5px solid #2d3348 !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input::placeholder { color: #4a5568 !important; }
.stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.12) !important;
}

/* ── Filter labels (Genre, Language, Année, Note) ── */
.stTextInput label,
.stSlider label,
.stMultiSelect label,
[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
}

/* ── Global Nuclear: Kill any remaining red from Streamlit primary color ──
   Streamlit injects its primaryColor into various elements via style attributes
   and CSS variables. This block resets them all to our teal theme. */
:root {
    --streamlit-color-red: #38bdf8;
    --primary-color: #38bdf8;
}
/* Any element Streamlit colors with the primaryColor that we haven't explicitly targeted */
[style*="color: rgb(229, 9, 20)"],
[style*="color: rgb(255, 75, 75)"],
[style*="background-color: rgb(229, 9, 20)"],
[style*="background-color: rgb(255, 75, 75)"],
[style*="border-color: rgb(229, 9, 20)"],
[style*="border-color: rgb(255, 75, 75)"] {
    color: #38bdf8 !important;
    background-color: rgba(56,189,248,0.12) !important;
    border-color: rgba(56,189,248,0.4) !important;
}

/* ── Single-select dropdowns (Sort by, etc.) ── */
[data-baseweb="select"] { border-radius: 10px !important; overflow: hidden; }
[data-baseweb="select"] > div {
    background-color: #1a1d27 !important;
    border: 1.5px solid #2d3348 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    min-height: 40px !important;
    transition: border-color 0.2s !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1) !important;
}
/* Placeholder text */
[data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"] span,
[data-baseweb="select"] div[class*="placeholder"],
[data-baseweb="select"] input::placeholder {
    color: #6b7ea0 !important;
}
/* Selected value text */
[data-baseweb="select"] span,
[data-baseweb="select"] div[class*="singleValue"],
[data-baseweb="select"] div[class*="value"] {
    color: #d4ddf0 !important;
}
/* Dropdown arrow icon */
[data-baseweb="select"] svg { color: #6b7ea0 !important; fill: #6b7ea0 !important; }
/* Dropdown list */
[data-baseweb="popover"] { background: #1a1d27 !important; border: 1px solid #2d3348 !important; border-radius: 10px !important; }
[data-baseweb="menu"] { background: #1a1d27 !important; border-radius: 10px !important; }
[role="option"] { background: #1a1d27 !important; color: #d4ddf0 !important; font-size: 0.85rem !important; }
[role="option"]:hover,
[role="option"][aria-selected="true"] { background: #252d45 !important; color: #e2e8f0 !important; }



/* ── Top10 genre pills (st.radio horizontal) ── */
div[data-testid="stRadio"] > div {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
}
div[data-testid="stRadio"] label {
    background: #1e2235 !important;
    border: 1px solid #2d3855 !important;
    border-radius: 20px !important;
    padding: 5px 16px 5px 12px !important;
    color: #94a3b8 !important;
    cursor: pointer !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 0px !important;
}
/* ── Hide the native radio visual indicator (the circle/dot) ──
   Streamlit renders a <div> containing the circular SVG/styled element
   as the FIRST child inside the label. We hide it completely. */
div[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}
/* ── Also hide via p element which sometimes wraps the dot ── */
div[data-testid="stRadio"] label > div[data-testid="stWidgetLabel"] > div:first-child {
    display: none !important;
}
/* ── Hide the raw <input> too ── */
div[data-testid="stRadio"] label input {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
}
/* ── Active/selected pill ── */
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(56, 189, 248, 0.13) !important;
    border-color: #38bdf8 !important;
    color: #7dd3fc !important;
    font-weight: 600 !important;
}
/* ── Hover state ── */
div[data-testid="stRadio"] label:hover {
    background: #252d42 !important;
    border-color: #3d5070 !important;
    color: #cbd5e1 !important;
}
/* ── Radio text <p> inside label ── */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
    color: inherit !important;
    font-size: 0.8rem !important;
    font-weight: inherit !important;
    margin: 0 !important;
    padding: 0 !important;
}



/* ── Section titles ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    border-left: 3px solid #38bdf8;
    padding-left: 12px;
    margin: 1.4rem 0 0.9rem;
    letter-spacing: 0.2px;
}

/* ─────────────────────────────────────────────────────────────────────────
   SLIDER — Comprehensive fix for Streamlit slider red-track issue.
   Streamlit applies its primaryColor as inline style on the active track
   element and thumb. We override via every known selector pattern.
   ───────────────────────────────────────────────────────────────────────── */

/* 1. Streamlit CSS custom property override (affects native theme engine) */
:root {
    --primary: #38bdf8 !important;
    --primaryColor: #38bdf8 !important;
}

/* 2. Thumb / handle */
[data-testid="stSlider"] [role="slider"],
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"],
[data-testid="stSlider"] div[role="slider"] {
    background: #38bdf8 !important;
    background-color: #38bdf8 !important;
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 5px rgba(56, 189, 248, 0.18) !important;
    outline: none !important;
}
[data-testid="stSlider"] [role="slider"]:focus,
[data-testid="stSlider"] [role="slider"]:active {
    box-shadow: 0 0 0 6px rgba(56, 189, 248, 0.28) !important;
}

/* 3. Active track fill — Streamlit injects inline style="background: rgb(255,...)"
      We need attribute selectors to override inline styles */
[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"],
[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background-color"] {
    background-color: #38bdf8 !important;
    background: #38bdf8 !important;
}

/* 4. The internal slider track structure (Streamlit 1.28+):
      > div[0] = outer container
        > div[0] = track background (full width)
          > div[0] = filled portion (inline styled with primaryColor)
          > div[1] = empty portion
        > div[1] = thumb */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child > div:first-child {
    background-color: #38bdf8 !important;
    background: #38bdf8 !important;
}

/* 5. Track background (unfilled portion) */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    background-color: #2d3348 !important;
    border-radius: 4px !important;
}

/* 6. Min/Max value labels */
[data-testid="stSlider"] p,
[data-testid="stTickBarMin"],
[data-testid="stTickBarMax"] {
    color: #64748b !important;
    font-size: 0.72rem !important;
}



/* ── Top-10 card ── */
.top10-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #1a1d27;
    border: 1px solid #252a37;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    cursor: pointer;
    margin-bottom: 4px;
}
.top10-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.45);
    border-color: rgba(56, 189, 248, 0.45);
}
.top10-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
}
.top10-no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1d27, #252a37);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3d4560;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Rank badge (outside poster, in meta area) ── */
.top10-meta {
    background: #141720;
    padding: 8px 10px 10px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.top10-rank-badge {
    flex-shrink: 0;
    width: 22px;
    height: 22px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 1px;
}
.top10-text { flex: 1; min-width: 0; }
.top10-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #e2e8f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
    line-height: 1.35;
}
.top10-rating {
    font-size: 0.65rem;
    color: #94a3b8;
    font-weight: 500;
}
.top10-rating .rating-value {
    color: #fbbf24;
    font-weight: 700;
}

/* ── Results grid card ── */
.result-card {
    background: #1a1d27;
    border: 1px solid #252a37;
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
    margin-bottom: 4px;
}
.result-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56, 189, 248, 0.45);
    box-shadow: 0 10px 28px rgba(0,0,0,0.4);
}
.result-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.result-card-no-poster {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #1a1d27, #252a37);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3d4560;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.result-card-body { padding: 10px 11px 12px; background: #141720; }
.result-card-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #f1f5f9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 3px;
    line-height: 1.35;
}
.result-card-meta { font-size: 0.72rem; color: #64748b; margin-bottom: 5px; }

/* ── Rating progress bar ── */
.rating-wrap { display: flex; align-items: center; gap: 7px; margin: 5px 0; }
.rating-track {
    flex: 1;
    height: 5px;
    background: #2d3348;
    border-radius: 3px;
    overflow: hidden;
}
.rating-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #fbbf24, #f59e0b);
}
.rating-label { font-size: 0.75rem; font-weight: 700; color: #fbbf24; white-space: nowrap; }

/* ── Genre badges ── */
.badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 12px;
    font-size: 0.67rem;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    margin-right: 4px;
    margin-bottom: 4px;
    letter-spacing: 0.2px;
}

/* ── Detail panel ── */
.detail-synopsis {
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.65;
    margin: 8px 0 14px;
}
.detail-meta { color: #94a3b8; font-size: 0.82rem; margin-bottom: 12px; }
.cast-strip { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 10px; }
.cast-item { text-align: center; width: 68px; }
.cast-photo {
    width: 58px; height: 58px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #2d3348;
    display: block;
    margin: 0 auto;
}
.cast-no-photo {
    width: 58px; height: 58px;
    border-radius: 50%;
    background: #252a37;
    border: 2px solid #2d3348;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    color: #4a5568;
    margin: 0 auto;
}
.cast-name { font-size: 0.6rem; color: #94a3b8; margin-top: 4px; word-break: break-word; line-height: 1.3; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 1rem;
    color: #4a5568;
}
.empty-state .empty-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
    color: #2d3348;
}
.empty-state p { font-size: 1rem; color: #64748b; margin: 0.3rem 0; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #1a1d27 !important;
    border: 1px solid #252a37 !important;
    border-radius: 10px !important;
}

/* ── Buttons (global) ── */
.stButton > button {
    background: #1a1d27 !important;
    color: #94a3b8 !important;
    border: 1px solid #2d3348 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #252a37 !important;
    color: #e2e8f0 !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
}

/* ── Result count badge ── */
.count-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.22);
    color: #94a3b8;
    font-size: 0.76rem;
    font-weight: 500;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
    letter-spacing: 0.2px;
}
.count-badge strong { color: #38bdf8; font-weight: 700; }

/* ── Multiselect — dark theme ── */
[data-baseweb="multi-select"] { border-radius: 10px !important; overflow: hidden; }
[data-baseweb="multi-select"] > div {
    background-color: #1a1d27 !important;
    border: 1.5px solid #2d3348 !important;
    border-radius: 10px !important;
    min-height: 40px !important;
    transition: border-color 0.2s !important;
}
[data-baseweb="multi-select"] > div:focus-within {
    border-color: #38bdf8 !important;
}
/* Selected tag pills */
[data-baseweb="tag"] {
    background: rgba(56, 189, 248, 0.14) !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    border-radius: 8px !important;
}
[data-baseweb="tag"] span { color: #38bdf8 !important; font-size: 0.72rem !important; font-weight: 600 !important; }
[data-baseweb="tag"] button { color: rgba(56, 189, 248, 0.7) !important; }
[data-baseweb="tag"] button:hover { color: #38bdf8 !important; }
/* Dropdown list items */
[data-baseweb="menu"] li { color: #cbd5e1 !important; background: #1a1d27 !important; }
[data-baseweb="menu"] li:hover { background: #252a37 !important; }

/* ── Card container (visual + button stacking) ── */
.st-card-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    gap: 6px;
}

/* Card detail button (scoped) */
.st-card-container div[data-testid="stButton"] button {
    width: 100%;
    background-color: transparent !important;
    color: #64748b !important;
    border: 1px solid #252a37 !important;
    border-radius: 7px !important;
    padding: 0.45rem !important;
    font-weight: 500 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.22s ease !important;
}
.st-card-container div[data-testid="stButton"] button:hover {
    background-color: rgba(56, 189, 248, 0.08) !important;
    color: #38bdf8 !important;
    border-color: rgba(56, 189, 248, 0.35) !important;
    box-shadow: none !important;
}

/* Card hover states */
.st-card-container .top10-card:hover,
.st-card-container .result-card:hover {
    transform: translateY(-4px);
    border-color: rgba(56, 189, 248, 0.45);
    box-shadow: 0 10px 28px rgba(0,0,0,0.4);
}

/* ── Search Form ── */
[data-testid="stForm"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ── Form submit button ── */
[data-testid="stForm"] div[data-testid="stButton"] button {
    background: rgba(56, 189, 248, 0.12) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stForm"] div[data-testid="stButton"] button:hover {
    background: rgba(56, 189, 248, 0.2) !important;
    border-color: #38bdf8 !important;
    color: #f1f5f9 !important;
}

</style>
"""


# ── 2. Genre badges ────────────────────────────────────────────────────────

def genre_badge_html(genre: str) -> str:
    """Retourne un <span> badge coloré pour un genre donné."""
    color = GENRE_COLORS.get(genre, "#4a5568")
    return f'<span class="badge" style="background:{color};">{genre}</span>'


def genre_badges_html(genres_str: str) -> str:
    """
    Reçoit une chaîne de genres séparés par '|' ou ','
    et retourne le HTML de tous les badges concatenés.
    """
    if not genres_str or str(genres_str) == "nan":
        return ""
    genres = [g.strip() for g in genres_str.replace("|", ",").split(",") if g.strip()]
    return "".join(genre_badge_html(g) for g in genres)


# ── 3. Top-10 card ─────────────────────────────────────────────────────────

def top10_card_html(rank: int, title: str, year, poster_url: str | None,
                    avg_rating=None) -> str:
    """
    Retourne le HTML d'une carte Top-10 premium :
    affiche + badge de rang discret dans la zone méta + titre + note.
    Le rang n'est plus superposé sur le poster.
    """
    year_str = str(int(year)) if str(year) != "nan" else "N/A"
    if poster_url:
        img_html = f'<img src="{poster_url}" alt="{title}" loading="lazy"/>'
    else:
        img_html = '<div class="top10-no-poster">No Poster</div>'

    safe_title = title.replace('"', "&quot;")
    if avg_rating is not None:
        _r = f"{float(avg_rating):.1f}"
        rating_html = (
            f'<div class="top10-rating">'
            f'<span class="rating-value">{_r}</span>'
            f'<span style="color:#64748b;font-weight:400;"> / 5</span>'
            f'</div>'
        )
    else:
        rating_html = '<div class="top10-rating" style="color:#3d4560;">—</div>'

    return f"""
<div class="top10-card" title="{safe_title} ({year_str})">
    {img_html}
    <div class="top10-meta">
        <div class="top10-rank-badge">{rank}</div>
        <div class="top10-text">
            <div class="top10-title">{title}</div>
            {rating_html}
        </div>
    </div>
</div>
"""


def search_card_html(title: str, year, poster_url: str | None,
                     avg_rating=None) -> str:
    """
    Carte compacte pour les résultats de recherche.
    Sans numéro de classement. Styles inline pour fiabilité dans st.markdown.
    """
    year_str = str(int(year)) if str(year) != "nan" else "N/A"
    if poster_url:
        img_html = f'<img src="{poster_url}" alt="{title}" loading="lazy" style="width:100%;aspect-ratio:2/3;object-fit:cover;display:block;"/>'
    else:
        img_html = '<div style="width:100%;aspect-ratio:2/3;background:linear-gradient(135deg,#1a1d27,#252a37);display:flex;align-items:center;justify-content:center;color:#3d4560;font-size:0.7rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;">No Poster</div>'

    safe_title = title.replace('"', "&quot;")
    if avg_rating is not None:
        _r = f"{float(avg_rating):.1f}"
        rating_html = (
            f'<div style="padding:0 8px 7px;font-size:0.65rem;color:#94a3b8;background:#141720;font-weight:500;">'
            f'<span style="color:#fbbf24;font-weight:700;">{_r}</span>'
            f'<span style="color:#4a5568;"> / 5</span>'
            f'</div>'
        )
    else:
        rating_html = ""

    return f"""
<div class="result-card" style="position:relative;border-radius:10px;overflow:hidden;background:#1a1d27;border:1px solid #252a37;margin-bottom:4px;" title="{safe_title} ({year_str})">
    {img_html}
    <div style="padding:7px 8px 4px;font-size:0.72rem;font-weight:600;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:#141720;">{title}</div>
    <div style="padding:0 8px 4px;font-size:0.65rem;color:#64748b;background:#141720;">{year_str}</div>
    {rating_html}
</div>
"""


# ── 4. Rating bar (BigQuery avg_rating /5) ─────────────────────────────────

def rating_bar_html(score, max_score: float = 5.0) -> str:
    """
    Retourne une barre de progression + label pour une note BigQuery.
    Échelle par défaut : /5 (avg_rating BigQuery).
    """
    if score is None:
        return ""
    try:
        pct = (float(score) / max_score) * 100
        _r = f"{float(score):.1f}"
    except (ValueError, TypeError):
        return ""
    return (
        f'<div class="rating-wrap">'
        f'<div class="rating-track">'
        f'<div class="rating-fill" style="width:{pct:.0f}%;"></div>'
        f'</div>'
        f'<span class="rating-label">{_r}<span style="color:#5a6478;font-weight:400;font-size:0.65rem;">/5</span></span>'
        f'</div>'
    )


# ── 5. Result grid card ────────────────────────────────────────────────────

def result_card_html(title: str, year, poster_url: str | None,
                     avg_rating, genres_str: str) -> str:
    """
    Retourne le HTML d'une carte résultat (grille 3 colonnes).
    avg_rating est la note BigQuery (/5) — None si non disponible.
    """
    year_str = str(int(year)) if str(year) != "nan" else "N/A"
    if poster_url:
        img_html = f'<img src="{poster_url}" alt="{title}" loading="lazy"/>'
    else:
        img_html = '<div class="result-card-no-poster">No Poster</div>'

    rating_html = rating_bar_html(avg_rating, max_score=5.0) if avg_rating else ""
    badges = genre_badges_html(genres_str)
    safe_title = title.replace('"', "&quot;")

    return f"""
<div class="result-card">
    {img_html}
    <div class="result-card-body">
        <div class="result-card-title" title="{safe_title}">{title}</div>
        <div class="result-card-meta">{year_str}</div>
        {rating_html}
        <div style="margin-top:6px;">{badges}</div>
    </div>
</div>
"""


# ── 6. Detail panel ────────────────────────────────────────────────────────

def detail_cast_html(credits: dict) -> str:
    """Retourne le HTML de la bande de casting (5 premiers acteurs)."""
    if not credits:
        return ""
    cast_list = credits.get("cast", [])[:5]
    if not cast_list:
        return ""
    items = []
    for actor in cast_list:
        profile = actor.get("profile_path")
        photo_url = f"https://image.tmdb.org/t/p/w185{profile}" if profile else None
        if photo_url:
            photo_html = f'<img class="cast-photo" src="{photo_url}" alt="{actor["name"]}" loading="lazy"/>'
        else:
            photo_html = '<div class="cast-no-photo">—</div>'
        items.append(
            f'<div class="cast-item">'
            f'{photo_html}'
            f'<div class="cast-name">{actor["name"]}</div>'
            f'</div>'
        )
    return f'<div class="cast-strip">{"".join(items)}</div>'


def detail_panel_html(details: dict, row_dict: dict) -> str:
    """
    Retourne le HTML complet de la fiche détail d'un film.
    NOTE : la note affichée est UNIQUEMENT la note BigQuery (avg_rating /5).
    TMDB est utilisé uniquement pour l'affiche, le synopsis, la durée et le casting.
    """
    overview = details.get("overview") or "Synopsis non disponible."
    runtime = details.get("runtime")
    release = (details.get("release_date") or "")[:4] or str(row_dict.get("release_year", "N/A"))

    # Genres depuis TMDB (plus propres) ou fallback BigQuery
    tmdb_genres = "|".join(g["name"] for g in details.get("genres", []))
    genres_str = tmdb_genres or str(row_dict.get("genres", ""))
    badges = genre_badges_html(genres_str)

    # Note : uniquement BigQuery avg_rating (/5)
    bq_rating = row_dict.get("avg_rating")
    rating_html = (
        rating_bar_html(bq_rating, max_score=5.0)
        if bq_rating is not None
        else '<p style="color:#4a5568;font-size:0.82rem;font-style:italic;">Note utilisateur non disponible pour ce film.</p>'
    )

    meta_parts = []
    if runtime:
        meta_parts.append(f"{runtime} min")
    meta_parts.append(f"{release}")
    lang = str(row_dict.get("language", "N/A")).upper()
    meta_parts.append(f"{lang}")
    meta_str = "&nbsp;·&nbsp;".join(
        f'<span style="color:#94a3b8;font-size:0.82rem;">{m}</span>'
        for m in meta_parts
    )

    credits = details.get("credits", {})
    cast_html = detail_cast_html(credits) if credits else ""

    return f"""
<div style="margin-bottom:6px;">{badges}</div>
<p class="detail-synopsis">{overview}</p>
{rating_html}
<p class="detail-meta" style="margin-top:8px;">{meta_str}</p>
{ '<p style="color:#f1f5f9;font-weight:600;margin:12px 0 4px;font-size:0.85rem;letter-spacing:0.5px;">Casting</p>' + cast_html if cast_html else '' }
"""


# ── 7. Empty state ─────────────────────────────────────────────────────────

def no_results_html() -> str:
    """Retourne le HTML de l'état vide (aucun résultat trouvé)."""
    return """
<div class="empty-state">
    <span class="empty-icon">◻</span>
    <p><strong style="color:#94a3b8;">Aucun film trouvé</strong></p>
    <p>Essayez un autre titre ou ajustez vos filtres.</p>
</div>
"""


# ── 8. Movie detail full page ───────────────────────────────────────────────

def movie_detail_page_html(
    *,
    title: str,
    year,
    genres_str: str,
    language_label: str,
    avg_rating,
    rating_count,
    details: dict,          # TMDB dict (poster, synopsis, runtime, credits, backdrop)
    poster_url: str | None,
) -> str:
    """
    Retourne le HTML complet de la page détail d'un film.

    Données BigQuery  : title, year, genres_str, language_label, avg_rating, rating_count
    Données TMDB      : details (synopsis, durée, casting, backdrop)
    Séparation stricte : les genres et la langue viennent TOUJOURS de BigQuery.
    """
    # ── Backdrop (TMDB) ──────────────────────────────────────────────────
    backdrop_path = details.get("backdrop_path") if details else None
    if backdrop_path:
        backdrop_css = f"background-image: linear-gradient(to right, rgba(10,12,18,0.98) 38%, rgba(10,12,18,0.6) 100%), url('https://image.tmdb.org/t/p/w1280{backdrop_path}'); background-size: cover; background-position: center top;"
    else:
        backdrop_css = "background: linear-gradient(135deg, #0f1117 0%, #141824 60%, #0f1a24 100%);"

    # ── Poster (TMDB) ────────────────────────────────────────────────────
    if poster_url:
        poster_html = f'<img src="{poster_url}" alt="{title}" style="width:100%;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,0.6);display:block;"/>'
    else:
        poster_html = '<div style="width:100%;aspect-ratio:2/3;background:linear-gradient(135deg,#1a1d27,#252a37);border-radius:12px;display:flex;align-items:center;justify-content:center;color:#3d4560;font-size:0.75rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;">No Poster</div>'

    # ── Year ─────────────────────────────────────────────────────────────
    year_str = str(int(year)) if str(year) not in ("nan", "None", "") else "N/A"

    # ── Genres (BigQuery) ────────────────────────────────────────────────
    badges = genre_badges_html(genres_str)

    # ── Rating (BigQuery) ────────────────────────────────────────────────
    if avg_rating is not None:
        try:
            pct = (float(avg_rating) / 5.0) * 100
            _r = f"{float(avg_rating):.1f}"
            rating_block = f"""
<div style="margin:20px 0 16px;">
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
    <div style="background:rgba(251,191,36,0.08);border:1.5px solid rgba(251,191,36,0.35);border-radius:50%;width:64px;height:64px;display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0;">
      <span style="font-size:1.2rem;font-weight:900;color:#fbbf24;line-height:1;">{_r}</span>
      <span style="font-size:0.52rem;color:#64748b;font-weight:600;letter-spacing:0.5px;margin-top:1px;">/ 5</span>
    </div>
    <div style="flex:1;min-width:100px;">
      <div style="font-size:0.65rem;color:#4a5568;margin-bottom:6px;font-weight:700;letter-spacing:1px;text-transform:uppercase;">Note utilisateur</div>
      <div style="height:6px;background:#1e2233;border-radius:3px;overflow:hidden;">
        <div style="height:100%;width:{pct:.0f}%;background:linear-gradient(90deg,#fbbf24,#f59e0b);border-radius:3px;"></div>
      </div>
      <div style="font-size:0.7rem;color:#4a5568;margin-top:5px;">{int(rating_count) if rating_count else '?'} avis</div>
    </div>
  </div>
</div>"""
        except Exception:
            rating_block = ""
    else:
        rating_block = '<p style="color:#4a5568;font-style:italic;font-size:0.82rem;margin:16px 0;">Note utilisateur non disponible.</p>'

    # ── TMDB data ────────────────────────────────────────────────────────
    if details:
        overview  = details.get("overview") or ""
        runtime   = details.get("runtime")
        credits   = details.get("credits", {})
    else:
        overview  = ""
        runtime   = None
        credits   = {}

    synopsis_block = (
        f'<p style="color:#cbd5e1;font-size:0.92rem;line-height:1.7;margin:0 0 18px;">{overview}</p>'
        if overview else
        '<p style="color:#4a5568;font-style:italic;font-size:0.85rem;">Synopsis non disponible.</p>'
    )

    # ── Meta row ─────────────────────────────────────────────────────────
    meta_items = [f'<span style="color:#e2e8f0;font-weight:600;">{year_str}</span>']
    if runtime:
        h, m = divmod(int(runtime), 60)
        meta_items.append(f'<span style="color:#64748b;">{h}h {m:02d}min</span>')
    if language_label:
        meta_items.append(f'<span style="background:#1a1d27;border:1px solid #2d3348;border-radius:6px;padding:2px 10px;color:#94a3b8;font-size:0.76rem;">{language_label}</span>')
    meta_html = '<span style="color:#2d3348;margin:0 6px;">·</span>'.join(meta_items)

    # ── Casting (TMDB) ───────────────────────────────────────────────────
    cast_list = credits.get("cast", [])[:6]
    if cast_list:
        cast_items = []
        for actor in cast_list:
            profile = actor.get("profile_path")
            if profile:
                img = f'<img src="https://image.tmdb.org/t/p/w185{profile}" alt="{actor["name"]}" style="width:58px;height:58px;border-radius:50%;object-fit:cover;border:2px solid #2d3348;display:block;margin:0 auto;"/>'
            else:
                img = '<div style="width:58px;height:58px;border-radius:50%;background:#1e2233;border:2px solid #2d3348;display:flex;align-items:center;justify-content:center;font-size:1rem;color:#3d4560;margin:0 auto;">—</div>'
            cast_items.append(
                f'<div style="text-align:center;flex-shrink:0;width:70px;">'
                f'{img}'
                f'<div style="font-size:0.58rem;color:#64748b;margin-top:5px;word-break:break-word;line-height:1.3;">{actor["name"]}</div>'
                f'</div>'
            )
        cast_section = (
            '<p style="color:#94a3b8;font-weight:700;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;margin:22px 0 10px;">Casting</p>'
            '<div style="display:flex;flex-wrap:wrap;gap:12px;">' + "".join(cast_items) + '</div>'
        )
    else:
        cast_section = ""

    return f"""<div style="{backdrop_css}border-radius:16px;padding:36px 32px;margin-bottom:24px;border:1px solid #1e2233;">
<div style="display:grid;grid-template-columns:200px 1fr;gap:32px;align-items:start;">
<div style="flex-shrink:0;">
{poster_html}
</div>
<div>
<h2 style="font-size:1.9rem;font-weight:800;color:#f1f5f9;margin:0 0 8px;line-height:1.2;">{title}</h2>
<div style="display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:14px;font-size:0.82rem;">
{meta_html}
</div>
<div style="margin-bottom:6px;">{badges}</div>
{rating_block}
<p style="color:#4a5568;font-size:0.68rem;font-weight:700;letter-spacing:1.2px;margin:0 0 7px;text-transform:uppercase;">Synopsis</p>
{synopsis_block}
{cast_section}
</div>
</div>
</div>"""
