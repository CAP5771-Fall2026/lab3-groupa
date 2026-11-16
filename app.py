"""
Streamlit app: Spotify audio-feature correlation heatmap.

Recreates the Part 1 notebook visualization with interactive filters.
"""

from pathlib import Path

import kagglehub
import pandas as pd
import plotly.express as px
import streamlit as st

FEATURE_COLS = [
    "popularity",
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence",
]


@st.cache_data(show_spinner="Downloading Spotify dataset…")
def load_data() -> pd.DataFrame:
    dataset_path = Path(
        kagglehub.dataset_download("zaheenhamidani/ultimate-spotify-tracks-db")
    )
    csv_files = list(dataset_path.rglob("*.csv"))
    if len(csv_files) != 1:
        raise RuntimeError(f"Expected one CSV; found: {csv_files}")
    return pd.read_csv(csv_files[0])


st.set_page_config(
    page_title="Spotify Feature Heatmap",
    page_icon="🎵",
    layout="wide",
)

st.title("Spotify Tracks — Feature Correlation Heatmap")
st.markdown(
    """
Explore how Spotify audio features relate to each other using a correlation
heatmap. Use the sidebar filters to focus on genres, popularity ranges, and
which features appear in the matrix.
"""
)

df = load_data()

st.sidebar.header("Filters")

genres = sorted(df["genre"].dropna().unique())
selected_genres = st.sidebar.multiselect(
    "Genre",
    options=genres,
    default=genres[:8] if len(genres) >= 8 else genres,
    help="Limit the correlation calculation to tracks in these genres.",
)

min_pop, max_pop = int(df["popularity"].min()), int(df["popularity"].max())
popularity_range = st.sidebar.slider(
    "Popularity range",
    min_value=min_pop,
    max_value=max_pop,
    value=(min_pop, max_pop),
    help="Keep tracks whose popularity falls within this range.",
)

selected_features = st.sidebar.multiselect(
    "Features in heatmap",
    options=FEATURE_COLS,
    default=FEATURE_COLS,
    help="Choose which numeric features to include in the correlation matrix.",
)

color_scale = st.sidebar.selectbox(
    "Color scale",
    options=["RdBu_r", "Viridis", "Plasma", "IceFire", "Temps"],
    index=0,
)

filtered = df.copy()
if selected_genres:
    filtered = filtered[filtered["genre"].isin(selected_genres)]
else:
    st.sidebar.warning("No genres selected — showing all genres.")

lo, hi = popularity_range
filtered = filtered[
    (filtered["popularity"] >= lo) & (filtered["popularity"] <= hi)
]

col1, col2, col3 = st.columns(3)
col1.metric("Tracks in filter", f"{len(filtered):,}")
col2.metric("Genres selected", len(selected_genres) if selected_genres else len(genres))
col3.metric("Features selected", len(selected_features))

st.subheader("Dataset overview")
st.markdown(
    """
The app uses the **Ultimate Spotify Tracks DB** from Kaggle
(`zaheenhamidani/ultimate-spotify-tracks-db`): ~233k tracks with metadata
(genre, artist, track name) and audio features such as energy, danceability,
acousticness, loudness, and valence.
"""
)

if len(selected_features) < 2:
    st.error("Select at least two features to compute a correlation heatmap.")
    st.stop()

if filtered.empty:
    st.error("No tracks match the current filters. Widen the popularity range or add genres.")
    st.stop()

corr = filtered[selected_features].corr(numeric_only=True)

st.subheader("Correlation heatmap")
fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale=color_scale,
    zmin=-1,
    zmax=1,
    aspect="auto",
    labels=dict(color="Correlation"),
    title="Interactive Correlation Heatmap of Spotify Audio Features",
)
fig.update_layout(
    height=700,
    xaxis_title="Audio feature",
    yaxis_title="Audio feature",
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Interpretation"):
    st.markdown(
        """
- **Energy and loudness** are typically strongly positively correlated.
- **Acousticness** usually moves opposite to energy and loudness.
- **Danceability and valence** often rise together (upbeat / danceable tracks).
- **Popularity** usually shows only modest correlations with individual audio traits.

Adjust the sidebar filters to see how these relationships change across genres
or popularity bands.
"""
    )

st.caption("Built for Lab 3 Part 3 — Streamlit deployment of the Spotify heatmap notebook.")
