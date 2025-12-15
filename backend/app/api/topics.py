from fastapi import APIRouter, HTTPException

from ..core.scheduler import current_topics, enqueue_run, refresh_topics, replace_slot
from ..core.pipeline import create_run

router = APIRouter(prefix="/api/topics", tags=["topics"])


@router.get("/current")
async def get_current_topics():
    return current_topics()


@router.post("/{slot_id}/select")
async def select_topic(slot_id: str):
    batch = current_topics()
    topic = next((t for t in batch.get("topics", []) if t.get("slot") == slot_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    run = create_run(prompt=topic["launch_prompt"], pipeline="lite", mode="live")
    enqueue_run(run["run_id"])
    updated_batch = replace_slot(slot_id)
    return {"run_id": run["run_id"], "batch": updated_batch}


@router.post("/refresh")
async def refresh_topics_endpoint():
    return refresh_topics()
