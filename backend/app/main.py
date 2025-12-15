from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import projects, runs, templates, topics
from .core.scheduler import enqueue_run, schedule_weekly_refresh, start_workers
from .core.scheduler import current_topics

app = FastAPI(title="CouncilLab")
app.include_router(runs.router)
app.include_router(templates.router)
app.include_router(projects.router)
app.include_router(topics.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    start_workers()
    schedule_weekly_refresh()
    current_topics()  # ensure seed batch exists


@app.get("/")
async def root():
    return {"status": "ok", "message": "CouncilLab backend"}
