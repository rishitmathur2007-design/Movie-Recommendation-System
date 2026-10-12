import os
import pickle
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables. Streamlit deployment can use st.secrets.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TMDB_API_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def get_tmdb_credentials():
    """Return TMDB request headers and query parameters from configured secrets."""
    try:
        access_token = st.secrets.get("TMDB_ACCESS_TOKEN")
        api_key = st.secrets.get("TMDB_API_KEY")
    except Exception:
        # A local setup may not have .streamlit/secrets.toml.
        access_token = None
        api_key = None

    access_token = access_token or os.getenv("TMDB_ACCESS_TOKEN")
    api_key = api_key or os.getenv("TMDB_API_KEY")

    if access_token:
        return {"Authorization": f"Bearer {access_token}"}, {}
    if api_key:
        return {}, {"api_key": api_key}

    raise RuntimeError(
        "TMDB credentials are missing. Add TMDB_ACCESS_TOKEN or TMDB_API_KEY "
        "to your local .env file or Streamlit Secrets."
    )


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_poster(movie_id):
    """Fetch a poster URL; return None when the movie has no poster."""
    headers, params = get_tmdb_credentials()
    params = {**params, "language": "en-US"}

    response = requests.get(
        f"{TMDB_API_URL}/{movie_id}",
        headers=headers,
        params=params,
        timeout=15,
    )
    response.raise_for_status()

    poster_path = response.json().get("poster_path")
    if not poster_path:
        return None
    return f"{TMDB_IMAGE_URL}/{poster_path.lstrip('/')}"


@st.cache_resource
def load_movie_data():
    """Load the trusted, repository-provided movie catalogue and similarity matrix."""
    movie_path = DATA_DIR / "movie_list.pickle"
    similarity_path = DATA_DIR / "similarity.pickle"

    missing_files = [
        path.name for path in (movie_path, similarity_path) if not path.is_file()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Required data file(s) are missing: "
            + ", ".join(missing_files)
            + ". Make sure Git LFS is installed and run 'git lfs pull'."
        )

    with movie_path.open("rb") as file:
        movie_data = pickle.load(file)
    with similarity_path.open("rb") as file:
        similarity_data = pickle.load(file)

    if "title" not in movie_data.columns or "movie_id" not in movie_data.columns:
        raise ValueError("The movie catalogue must contain title and movie_id columns.")
    if len(movie_data) != len(similarity_data):
        raise ValueError(
            "The movie catalogue and similarity matrix have different lengths."
        )

    return movie_data, similarity_data


def recommend(movie, movie_data, similarity_data):
    """Return up to five similar movie titles and their poster URLs."""
    matching_rows = movie_data.index[movie_data["title"] == movie].tolist()
    if not matching_rows:
        return []

    index = matching_rows[0]
    ranked_movies = sorted(
        enumerate(similarity_data[index]),
        key=lambda item: item[1],
        reverse=True,
    )

    recommendations = []
    for row_index, _score in ranked_movies:
        if row_index == index:
            continue

        row = movie_data.iloc[row_index]
        try:
            poster = fetch_poster(row.movie_id)
        except requests.RequestException:
            # A temporary TMDB/network issue should not hide the recommendations.
            poster = None

        recommendations.append((row.title, poster))
        if len(recommendations) == 5:
            break

    return recommendations


st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommendation System")
st.write("Choose a movie to discover five similar titles.")

try:
    movies, similarity = load_movie_data()
except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"Unable to load the movie data: {error}")
    st.stop()

movie_titles = movies["title"].dropna().astype(str).tolist()
if not movie_titles:
    st.error("The movie catalogue is empty.")
    st.stop()

selected_movie = st.selectbox("Select a movie", movie_titles)

if st.button("Show Recommendations", type="primary"):
    try:
        recommendations = recommend(selected_movie, movies, similarity)
    except RuntimeError as error:
        st.error(str(error))
        st.stop()
    except (IndexError, TypeError, ValueError) as error:
        st.error(f"Unable to generate recommendations: {error}")
        st.stop()

    if not recommendations:
        st.info("No recommendations were found for this movie.")
    else:
        columns = st.columns(len(recommendations))
        for column, (title, poster_url) in zip(columns, recommendations):
            with column:
                st.markdown(f"**{title}**")
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.caption("Poster unavailable")
