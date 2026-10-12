import os
import pickle

import requests
import streamlit as st
from dotenv import load_dotenv

# Load .env for local development. Deployment can use Streamlit Secrets.
load_dotenv()


def get_tmdb_credentials():
    """Return configured TMDB credentials without logging or displaying them."""
    try:
        secrets = st.secrets
        access_token = secrets.get("TMDB_ACCESS_TOKEN")
        api_key = secrets.get("TMDB_API_KEY")
    except Exception:
        # Local development may not have a Streamlit secrets file.
        access_token = None
        api_key = None

    access_token = access_token or os.getenv("TMDB_ACCESS_TOKEN")
    api_key = api_key or os.getenv("TMDB_API_KEY")

    if access_token:
        return {"Authorization": f"Bearer {access_token}"}, {}

    if api_key:
        return {"accept": "application/json"}, {"api_key": api_key}

    raise RuntimeError(
        "TMDB credentials are not configured. Set TMDB_ACCESS_TOKEN or "
        "TMDB_API_KEY in your local .env file or Streamlit Secrets."
    )


def fetch_poster(movie_id):
    """Fetch a movie poster from TMDB using externally configured credentials."""
    headers, params = get_tmdb_credentials()
    headers.setdefault("accept", "application/json")
    params = {**params, "language": "en-US"}

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()

    movie_data = response.json()
    poster_path = movie_data.get("poster_path")

    if not poster_path:
        return None

    return f"https://image.tmdb.org/t/p/w500/{poster_path}"


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distance = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    recommended_movie_name = []
    recommended_movie_poster = []

    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)

    return recommended_movie_name, recommended_movie_poster


st.header("Movie Recommendation System Using Machine Learning")

movies = pickle.load(open("data/movie_list.pickle", "rb"))
similarity = pickle.load(open("data/similarity.pickle", "rb"))
movies_list = movies["title"].values

selected_movie = st.selectbox(
    "Type/Select Move name to get recomendation",
    movies_list,
)

if st.button("Show Recommendation"):
    try:
        recommended_movie_name, recommended_movie_poster = recommend(
            selected_movie
        )

        columns = st.columns(5)
        for column, name, poster in zip(
            columns,
            recommended_movie_name,
            recommended_movie_poster,
        ):
            with column:
                st.text(name)
                if poster:
                    st.image(poster)
                else:
                    st.caption("Poster unavailable")

    except RuntimeError as error:
        st.error(str(error))
    except requests.RequestException:
        st.error(
            "Unable to retrieve movie information from TMDB. Check your "
            "network connection and TMDB credentials, then try again."
        )
