# ==============================================
# tmdb_client.py — Appels à l'API TMDB
# ==============================================

import requests
import streamlit as st
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL, TMDB_TIMEOUT


@st.cache_data(show_spinner=False)
def get_movie_details_tmdb(tmdb_id):
    """
    Récupère les détails d'un film depuis TMDB à partir de son tmdbId.
    Retourne : poster, synopsis, note, durée, casting.
    Retourne None si tmdb_id est invalide ou si l'appel échoue.
    """
    if not tmdb_id or str(tmdb_id) == "nan":
        return None
    url = f"{TMDB_BASE_URL}/movie/{int(tmdb_id)}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits"
    }
    try:
        response = requests.get(url, params=params, timeout=TMDB_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"[TMDB ERROR] Timeout pour tmdbId={tmdb_id}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[TMDB ERROR] HTTP {e} pour tmdbId={tmdb_id}")
        return None
    except Exception as e:
        print(f"[TMDB ERROR] Inattendu : {e}")
        return None


def get_poster_url(poster_path: str):
    """Construit l'URL complète d'une affiche TMDB."""
    if poster_path:
        return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    return None
