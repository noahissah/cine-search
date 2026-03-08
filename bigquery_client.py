# ==============================================
# bigquery_client.py — Requêtes SQL et connexion BigQuery
# ==============================================

import os
import streamlit as st
from google.cloud import bigquery
from config import (
    KEY_PATH, PROJECT_ID, MOVIES_TABLE, RATINGS_TABLE,
    SEARCH_LIMIT, FILTER_LIMIT, TOP10_LIMIT, GENRES_BLACKLIST
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH


@st.cache_resource
def get_client():
    """Initialise et retourne le client BigQuery (mis en cache)."""
    return bigquery.Client(project=PROJECT_ID)


@st.cache_data(ttl=3600)
def get_available_genres() -> list[str]:
    """
    Récupère dynamiquement tous les genres distincts disponibles dans la base.

    La colonne `genres` contient des valeurs concaténées par '|' (ex : "Drama|Romance").
    Stratégie : récupérer les valeurs brutes depuis BigQuery, parser côté Python
    pour extraire chaque genre individuel, dédupliquer et trier.

    Cache : 1h (ttl=3600) — la liste est stable, reset au redémarrage.
    """
    client = get_client()
    query = f"""
        SELECT DISTINCT genres
        FROM `{MOVIES_TABLE}`
        WHERE genres IS NOT NULL AND genres != ''
    """
    df = client.query(query).to_dataframe()
    genres_set: set[str] = set()
    for raw in df["genres"].dropna():
        for g in str(raw).replace("|", ",").split(","):
            g = g.strip()
            if g and g not in GENRES_BLACKLIST:
                genres_set.add(g)
    return sorted(genres_set)


@st.cache_data(ttl=3600)
def get_available_languages() -> list[str]:
    """
    Récupère dynamiquement toutes les langues distinctes disponibles dans la base.

    Cache : 1h (ttl=3600) — la liste est stable, reset au redémarrage.
    """
    client = get_client()
    query = f"""
        SELECT DISTINCT language
        FROM `{MOVIES_TABLE}`
        WHERE language IS NOT NULL AND language != ''
        ORDER BY language
    """
    df = client.query(query).to_dataframe()
    return [str(l) for l in df["language"].dropna().tolist() if str(l).strip()]


@st.cache_data(ttl=600)
def get_movie_by_id(movie_id: int):
    """
    Récupère les données BigQuery d'un film précis par son movieId.
    Utilisé pour la page détail du film.

    Retourne un dict avec tous les champs disponibles (title, genres, language,
    release_year, tmdbId, avg_rating, rating_count).
    Retourne None si introuvable.
    """
    client = get_client()
    query = f"""
        SELECT m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId,
               ROUND(AVG(r.rating), 2) AS avg_rating,
               COUNT(r.rating)         AS rating_count
        FROM `{MOVIES_TABLE}` m
        LEFT JOIN `{RATINGS_TABLE}` r ON m.movieId = r.movieId
        WHERE m.movieId = {int(movie_id)}
        GROUP BY m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId
        LIMIT 1
    """
    df = client.query(query).to_dataframe()
    if df.empty:
        return None
    row = df.iloc[0]
    return row.to_dict()


@st.cache_data(ttl=600)
def search_by_title(title: str):
    """
    Recherche des films dont le titre contient la chaîne donnée.
    Utilise SQL LIKE avec insensibilité à la casse.
    Résultat mis en cache 10 min (ttl=600) pour éviter les requêtes répétées.
    """
    client = get_client()
    # Échappement pour éviter les injections SQL
    title_clean = title.replace("'", "\\'")
    query = f"""
        SELECT movieId, title, genres, language, release_year, tmdbId
        FROM `{MOVIES_TABLE}`
        WHERE LOWER(title) LIKE LOWER('%{title_clean}%')
        LIMIT {SEARCH_LIMIT}
    """
    return client.query(query).to_dataframe()


def _build_search_clauses(title, genres, languages, min_year, max_year, min_rating, max_rating,
                          sort_by: str = "rating_desc"):
    """
    Construit les clauses WHERE, HAVING et ORDER BY communes à search_movies()
    et count_search_movies(). Centralise la logique pour éviter la duplication.

    sort_by : clé de tri (doit correspondre à une valeur dans config.SORT_OPTIONS)
      "rating_desc" → mieux notés en premier  (défaut)
      "rating_asc"  → moins bien notés en premier
      "year_desc"   → plus récents en premier
      "year_asc"    → plus anciens en premier

    Retourne un tuple : (where_clause, having_clause, order_clause)
    """
    conditions = []

    # Titre (insensible à la casse, LIKE %…%)
    if title and title.strip():
        t = title.strip().replace("'", "\\'")
        conditions.append(f"LOWER(m.title) LIKE LOWER('%{t}%')")

    # Genres : OR entre les valeurs sélectionnées
    if genres:
        gc = [f"m.genres LIKE '%{g.replace(chr(39), chr(92)+chr(39))}%'" for g in genres]
        conditions.append(f"({' OR '.join(gc)})")

    # Langues : IN clause
    if languages:
        ll = ", ".join(f"'{lg}'" for lg in languages)
        conditions.append(f"m.language IN ({ll})")

    # Année de sortie (Plage)
    if min_year is not None:
        conditions.append(f"m.release_year >= {int(min_year)}")
    if max_year is not None:
        conditions.append(f"m.release_year <= {int(max_year)}")

    where_clause  = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    
    # Notes (Plage de moyennes sur données agglomérées)
    having_conditions = []
    if min_rating is not None and min_rating > 0:
        having_conditions.append(f"AVG(r.rating) >= {min_rating}")
    if max_rating is not None and max_rating < 5.0:  # Optimization: 5.0 is the db max anyway
        having_conditions.append(f"AVG(r.rating) <= {max_rating}")
        
    having_clause = ("HAVING " + " AND ".join(having_conditions)) if having_conditions else ""

    # ORDER BY stable (toujours 4 clés pour garantir cohérence avec OFFSET)
    _ORDER_MAP = {
        "rating_desc": "ORDER BY avg_rating DESC NULLS LAST, rating_count DESC, title ASC, m.movieId ASC",
        "rating_asc":  "ORDER BY avg_rating ASC  NULLS LAST, rating_count ASC,  title ASC, m.movieId ASC",
        "year_desc":   "ORDER BY m.release_year DESC, avg_rating DESC NULLS LAST, title ASC, m.movieId ASC",
        "year_asc":    "ORDER BY m.release_year ASC,  avg_rating DESC NULLS LAST, title ASC, m.movieId ASC",
    }
    order_clause = _ORDER_MAP.get(sort_by, _ORDER_MAP["rating_desc"])

    return where_clause, having_clause, order_clause



@st.cache_data(ttl=300)
def count_search_movies(
    title: str = None,
    genres: list = None,
    languages: list = None,
    min_year: int = None,
    max_year: int = None,
    min_rating: float = None,
    max_rating: float = None,
) -> int:
    """
    Compte le nombre TOTAL de films correspondant aux critères de recherche,
    sans limite. Utilisé pour afficher "428 film(s) trouvé(s)" et déterminer
    si le bouton "Charger plus" doit apparaître.

    La requête principale est enveloppée dans un SELECT COUNT(*) AS total
    pour respecter les clauses HAVING de la requête imbriquée.
    """
    client = get_client()
    where_clause, having_clause, _ = _build_search_clauses(
        title, genres, languages, min_year, max_year, min_rating, max_rating
    )
    query = f"""
        SELECT COUNT(*) AS total
        FROM (
            SELECT m.movieId
            FROM `{MOVIES_TABLE}` m
            LEFT JOIN `{RATINGS_TABLE}` r ON m.movieId = r.movieId
            {where_clause}
            GROUP BY m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId
            {having_clause}
        )
    """
    result = client.query(query).to_dataframe()
    return int(result["total"].iloc[0]) if not result.empty else 0


@st.cache_data(ttl=300)
def search_movies(
    title: str = None,
    genres: list = None,
    languages: list = None,
    min_year: int = None,
    max_year: int = None,
    min_rating: float = None,
    max_rating: float = None,
    limit: int = None,
    offset: int = 0,
    sort_by: str = "rating_desc",
):
    """
    Fonction de recherche UNIFIÉE avec pagination LIMIT / OFFSET et tri.

    Paramètres de pagination :
    - limit   : nombre de résultats à retourner (défaut = FILTER_LIMIT)
    - offset  : position de départ pour la pagination (défaut = 0)
    - sort_by : clé de tri (voir SORT_OPTIONS dans config.py)
    """
    client = get_client()
    effective_limit = limit if limit is not None else FILTER_LIMIT
    where_clause, having_clause, order_clause = _build_search_clauses(
        title, genres, languages, min_year, max_year, min_rating, max_rating, sort_by=sort_by
    )
    query = f"""
        SELECT m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId,
               ROUND(AVG(r.rating), 2) AS avg_rating,
               COUNT(r.rating)         AS rating_count
        FROM `{MOVIES_TABLE}` m
        LEFT JOIN `{RATINGS_TABLE}` r ON m.movieId = r.movieId
        {where_clause}
        GROUP BY m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId
        {having_clause}
        {order_clause}
        LIMIT {effective_limit} OFFSET {offset}
    """
    return client.query(query).to_dataframe()


def filter_movies(language=None, genre=None, min_rating=None, min_year=None):
    """
    Filtre les films selon plusieurs critères combinables :
    - language : code ISO de la langue (ex: 'en', 'fr')
    - genre    : genre du film (ex: 'Comedy')
    - min_rating : note minimale moyenne — déclenche un JOIN + GROUP BY + HAVING
    - min_year   : année de sortie minimale

    Si min_rating est fourni, effectue un JOIN avec la table ratings
    pour calculer la moyenne via AVG() + GROUP BY + HAVING.
    """
    client = get_client()

    if min_rating:
        # Requête avec JOIN sur ratings pour calculer la note moyenne
        conditions = []
        if language:
            conditions.append(f"m.language = '{language}'")
        if genre:
            conditions.append(f"m.genres LIKE '%{genre}%'")
        if min_year:
            conditions.append(f"m.release_year >= {min_year}")
        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
            SELECT m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId,
                   ROUND(AVG(r.rating), 2) AS avg_rating
            FROM `{MOVIES_TABLE}` m
            JOIN `{RATINGS_TABLE}` r ON m.movieId = r.movieId
            {where_clause}
            GROUP BY m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId
            HAVING AVG(r.rating) >= {min_rating}
            ORDER BY avg_rating DESC
            LIMIT {FILTER_LIMIT}
        """
    else:
        # Requête simple sans JOIN
        conditions = []
        if language:
            conditions.append(f"language = '{language}'")
        if genre:
            conditions.append(f"genres LIKE '%{genre}%'")
        if min_year:
            conditions.append(f"release_year >= {min_year}")
        where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

        query = f"""
            SELECT movieId, title, genres, language, release_year, tmdbId
            FROM `{MOVIES_TABLE}`
            {where_clause}
            ORDER BY release_year DESC
            LIMIT {FILTER_LIMIT}
        """

    return client.query(query).to_dataframe()


@st.cache_data(ttl=3600)
def get_top10_by_genre(genre: str = None):
    """
    Retourne les 10 films les mieux notés (en moyenne) parmi les films
    ayant reçu au moins 50 notes.
    Si genre est fourni (ex: 'Action'), filtre via LIKE sur la colonne genres.

    Utilise : JOIN ratings + GROUP BY + HAVING + ORDER BY avg_rating DESC + LIMIT 10
    Résultat mis en cache 1h pour éviter des requêtes BigQuery répétées.
    """
    client = get_client()
    genre_filter = f"WHERE m.genres LIKE '%{genre}%'" if genre and genre != "Tous" else ""
    query = f"""
        SELECT m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId,
               ROUND(AVG(r.rating), 2) AS avg_rating,
               COUNT(r.rating)         AS rating_count
        FROM `{MOVIES_TABLE}` m
        JOIN `{RATINGS_TABLE}` r ON m.movieId = r.movieId
        {genre_filter}
        GROUP BY m.movieId, m.title, m.genres, m.language, m.release_year, m.tmdbId
        HAVING COUNT(r.rating) >= 50
        ORDER BY avg_rating DESC
        LIMIT {TOP10_LIMIT}
    """
    return client.query(query).to_dataframe()
