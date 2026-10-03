# Dockerfile - the recipe to build and run the whole website on a server.
# A hosting website reads this file, builds the app and starts it.
#
# Part 1 builds the React app, part 2 runs Flask (which also serves React).

# ----- Part 1: build React (needs Node.js) -----
FROM node:22-slim AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build                      # -> /frontend/dist

# ----- Part 2: the Python backend -----
FROM python:3.12-slim
WORKDIR /app

# PyTorch for CPU only: much smaller than the normal version (servers have no graphics card)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt ./
RUN grep -v "^torch" requirements.txt > requirements-server.txt \
    && pip install --no-cache-dir -r requirements-server.txt

# Download the Hugging Face model now, so the website starts faster
ENV HF_HOME=/app/.cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# Our code + the built React app from part 1
COPY *.py emotion_model_multi.joblib ./
COPY --from=frontend /frontend/dist ./frontend/dist

# The database lives in /app/data. The app runs as a normal user (not root), for safety.
ENV DB_FILE=/app/data/wellbeing.db
RUN mkdir -p /app/data && useradd --uid 1000 appuser && chown -R appuser /app
USER appuser

# gunicorn = a real web server. 1 worker, so the model is loaded only once (saves memory).
ENV PORT=7860
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120 app:app
