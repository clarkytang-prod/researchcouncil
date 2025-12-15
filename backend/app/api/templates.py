from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from ..core.storage import _path, list_items, load, save
from ..schemas.template import TemplateCreate

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("")
async def list_templates():
    return list_items("templates")


@router.post("")
async def create_template(payload: TemplateCreate):
    template_id = str(uuid4())
    record = {
        "id": template_id,
        "title": payload.title,
        "prompt": payload.prompt,
        "created_at": datetime.utcnow().isoformat(),
    }
    save("templates", template_id, record)
    return record


@router.put("/{template_id}")
async def update_template(template_id: str, payload: TemplateCreate):
    try:
        record = load("templates", template_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")
    record.update({"title": payload.title, "prompt": payload.prompt, "updated_at": datetime.utcnow().isoformat()})
    save("templates", template_id, record)
    return record


@router.delete("/{template_id}")
async def delete_template(template_id: str):
    path = _path("templates", template_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    path.unlink()
    return {"status": "deleted"}
