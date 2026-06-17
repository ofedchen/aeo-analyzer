# === STAGE 1: Build the Vite Frontend ===
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# === STAGE 2: Build the Python Dependencies ===
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=backend/requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# === STAGE 3: Final Production Runtime ===
FROM python:3.12-slim
WORKDIR /app

# Copy the python virtual environment
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy backend files
COPY backend/ ./backend/

# Copy the BUILT frontend static files from Stage 1 
# (Make sure your python app mounts 'frontend/dist' to serve it!)
COPY --from=frontend-builder /frontend/dist ./frontend/dist

EXPOSE 3006
WORKDIR /app/backend

CMD ["/venv/bin/python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=3006"]