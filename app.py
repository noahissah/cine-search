# ==============================================
# app.py — Interface Streamlit principale
# Orchestre l'interface en appelant :
#   - bigquery_client.py  (SQL / BigQuery)
#   - tmdb_client.py      (API TMDB : images, synopsis, casting)
#   - ui_components.py    (HTML/CSS → str)
# ==============================================

import re
import pandas as pd
import streamlit as st
from bigquery_client import (
    get_top10_by_genre, search_movies,
    count_search_movies, get_available_genres, get_available_languages,
    get_movie_by_id,
)
from tmdb_client import get_movie_details_tmdb, get_poster_url
from ui_components import (
    get_global_css,
    top10_card_html,
    search_card_html,
    result_card_html,
    detail_panel_html,
    no_results_html,
    movie_detail_page_html,
    genre_badges_html,
)
from config import (
    LANGUAGE_DISPLAY_MAP, format_language_label,
    MIN_YEAR_BOUND, MAX_YEAR_BOUND, MIN_RATING_BOUND, MAX_RATING_BOUND,
    MSG_LOADING_TOP10, MSG_SEARCHING, MSG_SORTING, MSG_LOADING_MORE, MSG_LOADING_DETAIL,
    FILTER_LIMIT, SORT_OPTIONS,
)

# Suppression des emojis dans les libellés de tri (SORT_OPTIONS peut contenir des emojis)
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "\u23E9-\u23F3"
    "\u231A-\u231B"
    "\u25AA-\u25FE"
    "\u2B50"
    "\u2B55"
    "]+",
    flags=re.UNICODE,
)

def _strip_emoji(text: str) -> str:
    """Supprime les emojis et nettoie les espaces résiduels."""
    return _EMOJI_RE.sub("", text).strip()

# Version épurée des options de tri (sans emojis, valeurs inchangées)
_SORT_OPTIONS_CLEAN: dict[str, str] = {
    _strip_emoji(k): v for k, v in SORT_OPTIONS.items()
}

# Configuration de la page (doit être le premier appel Streamlit)
st.set_page_config(
    page_title="CineSearch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Injection du CSS global (thème sombre)
st.markdown(get_global_css(), unsafe_allow_html=True)


# ==============================================
# COMPOSANTS UI
# ==============================================

def render_hero():
    """Bannière d'en-tête de l'application."""
    st.markdown(
        """
        <div class="cine-hero">
            <h1><span class="accent">Cine</span>Search</h1>
            <p>Explorez des milliers de films</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results_grid(df, cols: int = 5):
    """
    Affiche les résultats de recherche en grille (5 colonnes par défaut).
    Chaque carte montre le poster, le titre, l'année et la note.
    Un bouton par film permet d'accéder à la fiche détail.
    """
    chunks = [df.iloc[i: i + cols] for i in range(0, len(df), cols)]
    for chunk in chunks:
        columns = st.columns(cols)
        for col, (_, row) in zip(columns, chunk.iterrows()):
            with col:
                details = get_movie_details_tmdb(row.get("tmdbId"))
                poster_url = get_poster_url(details.get("poster_path")) if details else None
                bq_rating = row.get("avg_rating") if "avg_rating" in row.index else None

                st.markdown('<div class="st-card-container">', unsafe_allow_html=True)
                st.markdown(
                    search_card_html(
                        title=row["title"],
                        year=row["release_year"],
                        poster_url=poster_url,
                        avg_rating=bq_rating,
                    ),
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Découvrir le film",
                    key=f"detail_search_{row['movieId']}",
                    use_container_width=True,
                ):
                    st.session_state["selected_movie"]  = int(row["movieId"])
                    st.session_state["nav_origin"]       = "search"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


def render_top10_section():
    """
    Affiche la section Top 10 :
    - Filtrage par genre via boutons radio en pills
    - Grille 5 × 2 avec rang, poster, titre et note
    - Données chargées depuis BigQuery (cache 1h)
    """
    st.markdown(
        '<div class="section-title">Top 10 des recommandations</div>',
        unsafe_allow_html=True,
    )

    # Genres disponibles depuis BigQuery, avec "Tous" en premier
    _dyn_genres = get_available_genres()
    top10_genre_options = ["Tous"] + _dyn_genres

    selected_genre = st.radio(
        "Genre",
        options=top10_genre_options,
        horizontal=True,
        label_visibility="hidden",
    )

    with st.spinner(MSG_LOADING_TOP10):
        try:
            top10_df = get_top10_by_genre(
                genre=None if selected_genre == "Tous" else selected_genre
            )
        except Exception as e:
            st.error(f"Erreur BigQuery : {e}")
            return

    if top10_df.empty:
        st.markdown(no_results_html(), unsafe_allow_html=True)
        return

    # 2 rangées de 5 colonnes
    rows_slices = [top10_df.iloc[:5], top10_df.iloc[5:10]]
    for row_slice in rows_slices:
        if row_slice.empty:
            break
        cols = st.columns(5)
        for col, (_, row) in zip(cols, row_slice.iterrows()):
            rank = top10_df.index.get_loc(row.name) + 1
            with col:
                details = get_movie_details_tmdb(row.get("tmdbId"))
                poster_url = get_poster_url(details.get("poster_path")) if details else None
                avg = row.get("avg_rating")
                st.markdown('<div class="st-card-container">', unsafe_allow_html=True)
                st.markdown(
                    top10_card_html(rank, row["title"], row["release_year"], poster_url, avg),
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Découvrir le film",
                    key=f"detail_top10_{row['movieId']}",
                    use_container_width=True,
                ):
                    st.session_state["selected_movie"] = int(row["movieId"])
                    st.session_state["nav_origin"]      = "top10"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


# ==============================================
# PAGE DÉTAIL D'UN FILM
# ==============================================

def render_movie_detail(movie_id: int):
    """
    Affiche la page détail d'un film.

    Sources de données :
      - BigQuery : title, year, genres, language, avg_rating, rating_count
      - TMDB     : poster, synopsis, runtime, casting

    Navigation : bouton retour contextualisé (Top 10 ou résultats de recherche).
    """
    with st.spinner(MSG_LOADING_DETAIL):
        bq = get_movie_by_id(movie_id)
    if not bq:
        st.error("Film introuvable dans BigQuery.")
        if st.button("← Retour"):
            st.session_state.pop("selected_movie", None)
            st.rerun()
        return

    details    = get_movie_details_tmdb(bq.get("tmdbId"))
    poster_url = get_poster_url(details.get("poster_path")) if details else None

    origin = st.session_state.get("nav_origin", "top10")
    back_label = "← Retour aux résultats" if origin == "search" else "← Retour au Top 10"
    if st.button(back_label, key="back_btn"):
        st.session_state.pop("selected_movie", None)
        st.session_state.pop("nav_origin", None)
        st.rerun()

    st.markdown(
        '<div class="section-title">Fiche film</div>',
        unsafe_allow_html=True,
    )

    lang_code  = str(bq.get("language") or "").strip().lower()
    lang_label = format_language_label(lang_code) if lang_code else ""

    st.markdown(
        movie_detail_page_html(
            title          = str(bq.get("title", "N/A")),
            year           = bq.get("release_year"),
            genres_str     = str(bq.get("genres") or ""),
            language_label = lang_label,
            avg_rating     = bq.get("avg_rating"),
            rating_count   = bq.get("rating_count"),
            details        = details or {},
            poster_url     = poster_url,
        ),
        unsafe_allow_html=True,
    )


# ==============================================
# FONCTION PRINCIPALE
# ==============================================

def main():
    # Si un film est sélectionné, on affiche directement sa fiche
    if "selected_movie" in st.session_state:
        with st.spinner(MSG_LOADING_DETAIL):
            render_movie_detail(st.session_state["selected_movie"])
        return

    render_hero()

    # Restauration des paramètres de recherche depuis la session
    saved_params = st.session_state.get("search_params", {})

    if "search_input_key" not in st.session_state:
        st.session_state["search_input_key"] = saved_params.get("title", "")

    with st.form("search_form", clear_on_submit=False):
        search_col, btn_col = st.columns([7, 1])
        with search_col:
            title_input = st.text_input(
                "Recherche",
                key="search_input_key",
                placeholder="Rechercher le titre d'un film",
                label_visibility="collapsed",
            )
        with btn_col:
            search_clicked = st.form_submit_button("Rechercher", use_container_width=True)

    # Filtres inline (4 colonnes)
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        genres_selected = st.multiselect(
            "Genre",
            options=get_available_genres(),
            default=saved_params.get("genres", []),
            placeholder="Tous les genres",
        )
    with fc2:
        languages_selected = st.multiselect(
            "Language",
            options=get_available_languages(),
            default=saved_params.get("languages", []),
            format_func=format_language_label,
            placeholder="Toutes les langues",
        )
    with fc3:
        saved_min_year = saved_params.get("min_year", MIN_YEAR_BOUND)
        saved_max_year = saved_params.get("max_year", MAX_YEAR_BOUND)
        min_year, max_year = st.slider(
            "Année de sortie",
            min_value=MIN_YEAR_BOUND,
            max_value=MAX_YEAR_BOUND,
            value=(saved_min_year, saved_max_year),
        )
    with fc4:
        saved_min_rating = saved_params.get("min_rating", MIN_RATING_BOUND)
        saved_max_rating = saved_params.get("max_rating", MAX_RATING_BOUND)
        min_rating, max_rating = st.slider(
            "Note",
            min_value=MIN_RATING_BOUND,
            max_value=MAX_RATING_BOUND,
            value=(saved_min_rating, saved_max_rating),
            step=0.10,
            format="%.2f"
        )

    # Détermine si des critères de recherche sont actifs
    has_input = bool(
        (title_input or "").strip()
        or genres_selected
        or languages_selected
        or (min_year > MIN_YEAR_BOUND or max_year < MAX_YEAR_BOUND)
        or (min_rating > MIN_RATING_BOUND or max_rating < MAX_RATING_BOUND)
    )

    # Lancement de la recherche (réinitialise la pagination)
    if search_clicked:
        if not has_input:
            st.warning("Veuillez entrer un titre de film ou sélectionner au moins un filtre.")
        else:
            params = dict(
                title=(title_input or "").strip() or None,
                genres=genres_selected or None,
                languages=languages_selected or None,
                min_year=min_year,
                max_year=max_year,
                min_rating=min_rating,
                max_rating=max_rating,
                sort_by="rating_desc",
            )
            with st.spinner(MSG_SEARCHING):
                try:
                    st.session_state["search_params"]  = params
                    st.session_state["total_count"]    = count_search_movies(
                        **{k: v for k, v in params.items() if k != "sort_by"}
                    )
                    st.session_state["results_offset"] = FILTER_LIMIT
                    st.session_state["results"]        = search_movies(
                        **params, limit=FILTER_LIMIT, offset=0
                    )
                except Exception as e:
                    st.error(f"Erreur lors de la recherche : {e}")

    # Affichage des résultats (si présents dans la session)
    if "results" in st.session_state:
        results     = st.session_state["results"]
        total_count = st.session_state.get("total_count", len(results))
        curr_shown  = len(results)
        params      = st.session_state.get("search_params", {})
        offset      = st.session_state.get("results_offset", curr_shown)

        st.markdown('<div class="section-title">Résultats de recherche</div>', unsafe_allow_html=True)

        back_col, sort_col = st.columns([1, 2])
        with back_col:
            if st.button("← Retour au Top 10"):
                for key in ("results", "total_count", "results_offset", "search_params", "search_input_key"):
                    st.session_state.pop(key, None)
                st.rerun()
        with sort_col:
            sort_label = st.selectbox(
                "Trier par",
                options=list(_SORT_OPTIONS_CLEAN.keys()),
                index=0,
                key="sort_selector",
                label_visibility="visible",
            )
            new_sort_by = _SORT_OPTIONS_CLEAN[sort_label]

        # Relance la recherche si le tri change
        if new_sort_by != params.get("sort_by", "rating_desc"):
            updated_params = {**params, "sort_by": new_sort_by}
            with st.spinner(MSG_SORTING):
                try:
                    st.session_state["search_params"]  = updated_params
                    st.session_state["total_count"]    = count_search_movies(
                        **{k: v for k, v in updated_params.items() if k != "sort_by"}
                    )
                    st.session_state["results_offset"] = FILTER_LIMIT
                    st.session_state["results"]        = search_movies(
                        **updated_params, limit=FILTER_LIMIT, offset=0
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors du tri : {e}")

        st.markdown(
            f'<div class="count-badge"><strong>{total_count}</strong>&nbsp;film(s) trouvé(s)'
            f'&nbsp;·&nbsp;{curr_shown} affiché(s)</div>',
            unsafe_allow_html=True,
        )

        if results.empty:
            st.markdown(no_results_html(), unsafe_allow_html=True)
        else:
            render_results_grid(results, cols=5)

            if curr_shown < total_count:
                st.markdown("")
                _, center_col, _ = st.columns([1, 2, 1])
                with center_col:
                    if st.button(
                        f"Charger plus de résultats  ({curr_shown} / {total_count})",
                        use_container_width=True,
                        key="load_more_btn",
                    ):
                        with st.spinner(MSG_LOADING_MORE):
                            try:
                                next_batch = search_movies(
                                    **params, limit=FILTER_LIMIT, offset=offset
                                )
                                if not next_batch.empty:
                                    combined = pd.concat(
                                        [results, next_batch], ignore_index=True
                                    ).drop_duplicates(subset=["movieId"])
                                    st.session_state["results"]        = combined
                                    st.session_state["results_offset"] = offset + FILTER_LIMIT
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Erreur lors du chargement : {e}")
    else:
        # Page d'accueil : Top 10
        render_top10_section()


main()
