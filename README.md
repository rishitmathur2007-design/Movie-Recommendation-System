# 🎬 Movie Recommendation System

A content-based movie recommendation web app built with Python and Streamlit. Select a movie to receive up to five similar titles using a precomputed similarity matrix, with posters retrieved from TMDB.

**Live demo:** https://movie-recommendation-system-g4bshmbfoprsukqqcuzrpn.streamlit.app/

## Features

- Search/select a title from the movie catalogue.
- Generate up to five recommendations from the precomputed similarity matrix.
- Fetch movie posters from The Movie Database (TMDB).
- Cache movie data and poster requests to reduce repeated work.
- Show a helpful message when data files or TMDB credentials are missing.
- Keep API credentials outside the source code.

## Tech stack

- Python
- Streamlit
- Pandas / NumPy (for the stored movie data and similarity matrix)
- Requests
- python-dotenv
- Git LFS for the large precomputed pickle data files

## Project structure

```text
Movie-Recommendation-System/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── data/
    ├── movie_list.pickle
    └── similarity.pickle
```

The `.pickle` data files are tracked with Git LFS. If the repository checkout contains small text pointer files instead of the actual data, install Git LFS and run `git lfs pull`.

## Run locally

### 1. Clone the repository

Install Git and Git LFS first, then run:

```bash
git clone https://github.com/rishitmathur2007-design/Movie-Recommendation-System.git
cd Movie-Recommendation-System
git lfs install
git lfs pull
```

### 2. Create a virtual environment and install dependencies

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure TMDB

Copy `.env.example` to `.env` and set **one** credential:

```dotenv
TMDB_ACCESS_TOKEN=your_tmdb_read_access_token
# Alternatively, use an API key:
# TMDB_API_KEY=your_tmdb_api_key
```

Keep real credentials in `.env` only for local development. The file is ignored by Git. Never add credentials to source code or `.env.example`.

### 4. Start the app

```bash
streamlit run app.py
```

## Streamlit deployment

In the Streamlit app's **Settings → Secrets**, configure one of the following:

```toml
TMDB_ACCESS_TOKEN = "your_tmdb_read_access_token"
```

Or:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

Do not commit `.streamlit/secrets.toml`. The app reads Streamlit Secrets first and falls back to environment variables for local development.

## Security note

The current application source no longer embeds TMDB credentials. Previously committed credentials can remain visible in older Git history; removing a secret from the latest version does not erase it from earlier commits. Treat any credential that was publicly exposed as compromised and rotate/revoke it as appropriate. If history cleanup is required, follow [GitHub's sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Known limitations

- Recommendation quality depends on the precomputed catalogue and similarity matrix.
- TMDB poster images require network access and valid credentials; recommendations still display if a poster cannot be fetched.
- Pickle files must come from a trusted source because loading untrusted pickle data can execute code.
- The similarity matrix is large, so initial loading may take some time.

## Author

Rishit Mathur — https://github.com/rishitmathur2007-design
