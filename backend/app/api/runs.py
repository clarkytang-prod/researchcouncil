from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..core.pipeline import create_run
from ..core.scheduler import enqueue_run
from ..core.storage import list_items, load, save
from ..schemas.run import RunCreate

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.post("")
async def create_run_endpoint(payload: RunCreate):
    record = create_run(prompt=payload.prompt, pipeline=payload.pipeline, mode=payload.mode)
    if payload.mode == "live":
        enqueue_run(record["run_id"])
    else:
        record["status"] = "queued"
        save("runs", record["run_id"], record)
    return {"run_id": record["run_id"]}


@router.get("")
async def list_runs():
    runs = list_items("runs")
    summaries = [
        {
            "run_id": r.get("run_id"),
            "created_at": r.get("created_at"),
            "status": r.get("status"),
            "pipeline": r.get("pipeline"),
            "mode": r.get("mode"),
            "topic_prompt": r.get("topic_prompt"),
        }
        for r in runs
    ]
    return summaries


@router.get("/{run_id}")
async def get_run(run_id: str):
    try:
        return load("runs", run_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Run not found")


@router.get("/{run_id}/stream")
async def stream_run(run_id: str):
    # Simplified: return current run snapshot (SSE placeholder)
    try:
        run = load("runs", run_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Run not found")
    return JSONResponse(run)


@router.post("/{run_id}/rerun")
async def rerun(run_id: str):
    try:
        run = load("runs", run_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Run not found")
    run["status"] = "queued"
    save("runs", run_id, run)
    enqueue_run(run_id)
    return {"run_id": run_id, "status": "queued"}
