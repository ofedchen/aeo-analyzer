# AEO Validator — AI Search Readiness Checker

A full-stack web app that analyzes a website's readiness for LLM/AI search engines by inspecting `/llms.txt`, JSON-LD structured data, and page legibility. A two-agent CrewAI workflow (Technical Crawler → AEO Strategist) powered by Google Gemini produces a structured dashboard with scores and recommendations.

## Architecture

```
React (Vite/TS/Tailwind)  →  FastAPI  →  CrewAI Agents  →  Gemini API
                                    ↘  requests + BeautifulSoup (crawl)
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- [Google AI Studio](https://aistudio.google.com/apikey) API key (free tier)

## Quick Start

### 1. Backend

```bash
cd backend
cp .env.example .env
# Edit .env and set GEMINI_API_KEY

# Using uv (recommended)
uv venv && uv pip install -r requirements.txt
source .venv/bin/activate

# Phase 1 — CLI prototype
python main.py https://example.com

# Phase 2 — API server
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, enter a URL, and run the check.

Optional: set `VITE_API_BASE` in `frontend/.env` if the API is not on `http://127.0.0.1:8000`.

## API

**GET/POST** `/api/analyze?url=https://example.com`

Response schema:

```json
{
  "target_url": "https://example.com",
  "protocols": {
    "llms_txt_found": true,
    "json_ld_found": false
  },
  "metrics": {
    "legibility_score": 78
  },
  "analysis": {
    "summary": "...",
    "action_items": ["...", "..."]
  }
}
```

## Project Structure

```
aeo-validator/
├── backend/
│   ├── api.py          # FastAPI app + CORS
│   ├── main.py         # CLI entry (Phase 1)
│   ├── scraper.py      # Agent 1: crawl + protocol detection
│   ├── analyst.py      # Agent 2: CrewAI + Gemini analysis
│   ├── workflow.py     # Orchestration glue
│   └── schemas.py      # Shared Pydantic models
└── frontend/
    └── src/
        ├── App.tsx
        └── components/ # Dashboard, gauge, badges, insights
```

## Notes

- If `GEMINI_API_KEY` is missing, the backend falls back to heuristic scoring and rule-based recommendations.
- The frontend shows phased loading messages while the multi-agent analysis runs.
