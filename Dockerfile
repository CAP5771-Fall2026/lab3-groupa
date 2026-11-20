FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    KAGGLEHUB_CACHE=/opt/kagglehub \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

COPY requirements-app.txt .
RUN pip install -r requirements-app.txt

# Download the public Kaggle dataset at build time so the container
# starts quickly and works without network access.
RUN python -c "import kagglehub; print(kagglehub.dataset_download('zaheenhamidani/ultimate-spotify-tracks-db'))"

COPY app.py .

# Run as a non-root user.
RUN useradd --create-home appuser && chown -R appuser /app /opt/kagglehub
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
