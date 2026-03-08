# CineSearch – Exploration de films

CineSearch est une application Streamlit qui permet d’explorer un dataset de films stocké dans Google BigQuery.

L'application permet de :
- rechercher un film par titre
- filtrer par genre, langue, année et note
- afficher les informations détaillées d’un film
- consulter des recommandations de films

Les données sont interrogées directement depuis Google BigQuery et certaines informations complémentaires proviennent de l’API TMDB.

---

## Application en ligne

L'application est accessible à l'adresse suivante :

https://cine-search-975184994898.europe-west6.run.app

---

## Lancer l'application en local avec Docker

Construire l’image Docker :

```bash
docker build -t cine-search-app .