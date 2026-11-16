# lab3-groupa

Collaborative lab: interactive Spotify data visualization and deployment experiments (Voilà, Binder, Streamlit, Docker).

## Dataset

[Ultimate Spotify Tracks DB](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) — track metadata and audio features used in `visualize.ipynb`.

## Setup

1. Install [uv](https://github.com/astral-sh/uv) (or use pip).
2. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or with pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Open the notebook:

```bash
jupyter notebook visualize.ipynb
```

## Notebook

`visualize.ipynb` loads the Spotify dataset via `kagglehub`, describes the features, and shows:

- A danceability histogram
- An **interactive Plotly correlation heatmap** of audio features
- A short interpretation of the patterns

## Streamlit app (Part 3)

Run the interactive heatmap app locally:

```bash
source .venv/bin/activate
streamlit run app.py
```

Interactive controls in the sidebar:

- **Genre** multiselect filter
- **Popularity range** slider
- **Features in heatmap** multiselect
- **Color scale** dropdown

Screenshots of the running app are in `screenshots/`.
