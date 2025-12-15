# CouncilLab (MVP)

CouncilLab is a local-first web app for structured multi-model research. The backend is built with FastAPI and the frontend with Vite + React. Data is stored as auditable JSON files under `backend/data`.

## Getting started

1. **Install backend dependencies**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. **Set environment variables**

Copy `.env.example` to `.env` and set `OPENROUTER_API_KEY` if you want live LLM calls. Without a key, stub responses will be recorded.

```bash
cp .env.example .env
```

3. **Run the backend**

```bash
uvicorn app.main:app --reload --port 8000
```

4. **Run the frontend**

The frontend directory contains a minimal Vite/React skeleton.

```bash
cd frontend
npm install
npm run dev
```

## Council runs

- POST `/api/runs` with `{ "prompt": "...", "pipeline": "lite|deep", "mode": "live|overnight" }` to create a run.
- Live runs are enqueued immediately; overnight runs stay queued.
- Use `GET /api/runs/{run_id}` to inspect the saved `run.json`. Every stage stores prompts, responses, and cost placeholders.

## Weekly topics

- `GET /api/topics/current` returns the current five-slot batch (2 work, 2 education, 1 serendipity). A placeholder batch is generated on startup.
- `POST /api/topics/{slot}/select` launches a live Council Lite run seeded with that topic and replaces the slot with a fresh placeholder topic.
- `POST /api/topics/refresh` regenerates a new batch.

## Data storage

All content is stored as JSON under `backend/data`:

- Runs: `backend/data/runs/{run_id}.json`
- Templates: `backend/data/templates/{template_id}.json`
- Projects: `backend/data/projects/{project_id}.json`
- Topics: `backend/data/topics/{batch_id}.json`

You can export any run by copying its JSON file. The structure matches the council stages for auditability.
