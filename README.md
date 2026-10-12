# Movie Recommendation System

A Streamlit web application that recommends five movies similar to a selected title using a precomputed similarity matrix and displays their TMDB posters.

**Live demo:** https://movie-recommendation-system-g4bshmbfoprsukqqcuzrpn.streamlit.app/

## Features

- Select a movie from the available catalogue.
- Rank movies using the project's precomputed similarity matrix.
- Display five recommended movie titles.
- Retrieve poster images from The Movie Database (TMDB).
- Support local credentials through `.env` and deployment credentials through Streamlit Secrets.

## Technology

- Python
- Streamlit
- Requests
- Pandas
- python-dotenv
- Pickle-based precomputed movie catalogue and similarity data

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

The data files are stored with Git LFS. Install Git LFS and run `git lfs pull` if the actual data objects were not downloaded during cloning.

## Setup for local development

### 1. Clone the repository

```bash
git clone https://github.com/rishitmathur2007-design/Movie-Recommendation-System.git
cd Movie-Recommendation-System
git lfs pull
```

### 2. Create a virtual environment and install dependencies

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. Configure TMDB credentials

Copy `.env.example` to a new file named `.env`. Set **one** of the following variables using a newly issued TMDB credential:

- `TMDB_ACCESS_TOKEN` — TMDB API Read Access Token (Bearer token).
- `TMDB_API_KEY` — TMDB API key.

Do not put real credentials in `.env.example`, source code, screenshots, issues, or commits. The `.env` file is ignored by Git.

### 4. Run the application

```bash
streamlit run app.py
```

Choose a movie and select **Show Recommendation**.

## Streamlit deployment

In your Streamlit deployment's **Settings → Secrets**, add one of the following TOML entries:

```toml
TMDB_ACCESS_TOKEN = "paste-your-new-TMDB-read-access-token-here"
```

Or, if using an API key instead:

```toml
TMDB_API_KEY = "paste-your-new-TMDB-api-key-here"
```

Configure the secret in the deployment dashboard; do not commit `.streamlit/secrets.toml`. The app supports Streamlit Secrets first and falls back to environment variables loaded from `.env` for local development.

## Security notice

Credentials were previously embedded in `app.py`. Treat those credentials as exposed: revoke or rotate them in your TMDB account and use replacement credentials in local and deployment configuration. Removing credentials from the current source does not remove them from prior Git commits. Review the repository's history and follow GitHub's sensitive-data removal guidance if you need to purge the old values from history.

GitHub guidance: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

## Limitations

- Recommendations depend on the supplied, precomputed similarity matrix and movie dataset.
- Poster retrieval requires valid TMDB credentials and network access.
- Some movies may not have poster images available.
- The app loads pickle files; only use data files from a trusted source.

## Author

Rishit Mathur — https://github.com/rishitmathur2007-design
