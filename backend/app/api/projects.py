from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from ..core.storage import _path, list_items, load, save
from ..schemas.project import ProjectCreate

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
async def list_projects():
    return list_items("projects")


@router.post("")
async def create_project(payload: ProjectCreate):
    project_id = str(uuid4())
    record = {
        "id": project_id,
        "name": payload.name,
        "description": payload.description,
        "active": payload.active,
        "created_at": datetime.utcnow().isoformat(),
    }
    save("projects", project_id, record)
    return record


@router.put("/{project_id}")
async def update_project(project_id: str, payload: ProjectCreate):
    try:
        record = load("projects", project_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    record.update(
        {
            "name": payload.name,
            "description": payload.description,
            "active": payload.active,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )
    save("projects", project_id, record)
    return record


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    path = _path("projects", project_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    path.unlink()
    return {"status": "deleted"}
