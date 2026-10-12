# Movie Recommendation System

A content-based movie recommendation web app built with Streamlit. Choose a movie from the available dataset and the app displays five recommended titles with their posters.

**Live demo:** https://movie-recommendation-system-g4bshmbfoprsukqqcuzrpn.streamlit.app/

## How it works

1. The app loads the movie catalogue from `data/movie_list.pickle`.
2. It loads a precomputed similarity matrix from `data/similarity.pickle`.
3. After you select a movie and click **Show Recommendation**, it ranks titles using the selected movie's similarity scores.
4. It displays the five recommended titles and retrieves their posters from The Movie Database (TMDB).

The recommendation interface and runtime flow are implemented in `app.py`. The dataset is older, so movie availability and recommendations may not reflect recent releases.

## Features

- Movie selection through a Streamlit dropdown.
- Similarity-based recommendations for a selected title.
- Five recommended movie titles per selection.
- Movie poster retrieval through the TMDB API.
- Web interface suitable for running locally or deploying with Streamlit.

## Technology

- **Python**
- **Streamlit** — web interface
- **Pandas** — movie catalogue and title lookup
- **Pickle** — loading the precomputed catalogue and similarity data
- **Requests** — TMDB API requests
- **TMDB** — poster metadata and image URLs

The repository's existing project notes also identify NumPy, scikit-learn, NLTK, and Python's `ast` module in the project workflow. The current `app.py` imports Streamlit, Requests, and Pickle directly.

## Project files

```text
Movie-Recommendation-System/
├── app.py
├── data/
│   ├── movie_list.pickle
│   └── similarity.pickle
└── README.md
```

The two data files are stored using Git LFS pointers. Make sure Git LFS is installed and the actual data files are downloaded before running the app.

## Run locally

### Prerequisites

- Python 3.9 or a compatible Python version
- Git
- Git LFS, to retrieve the serialized data files
- A TMDB API credential configured securely for poster requests

### 1. Clone the repository

```bash
git clone https://github.com/rishitmathur2007-design/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

If Git LFS is installed, pull the tracked data objects if they were not downloaded during cloning:

```bash
git lfs pull
```

### 2. Install the runtime packages

```bash
python -m pip install streamlit requests pandas
```

### 3. Configure TMDB access

The current source contains a TMDB credential directly in `app.py`. Do not reuse or publish that credential. Revoke/rotate it in TMDB and update the application to read a replacement from an environment variable or Streamlit secrets before deploying or sharing the code. The app needs valid TMDB access to fetch posters.

### 4. Start the app

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open it in your browser, choose a movie, and click **Show Recommendation**.

## Known limitations

- The movie dataset is old and may not include newer titles.
- Recommendations depend on the precomputed similarity matrix supplied with the project.
- Poster retrieval depends on TMDB availability and valid credentials.
- The repository does not currently include a `requirements.txt`; the install command above lists the packages directly imported by the app, not a verified complete environment lockfile.
- The serialized pickle files must be downloaded correctly through Git LFS. Only load pickle files from sources you trust.

## Possible next improvements

- Move API credentials to Streamlit secrets or environment variables.
- Add a `requirements.txt` with tested dependency versions.
- Handle missing movie titles, absent poster paths, and API/network errors gracefully.
- Refresh the dataset and regenerate the similarity matrix.
- Add screenshots and automated checks for the recommendation flow.

## Author

**Rishit Mathur**  
GitHub: [@rishitmathur2007-design](https://github.com/rishitmathur2007-design)
