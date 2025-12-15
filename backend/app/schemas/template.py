from typing import Optional

from pydantic import BaseModel


class Template(BaseModel):
    id: str
    title: str
    prompt: str
    created_at: str
    updated_at: Optional[str] = None


class TemplateCreate(BaseModel):
    title: str
    prompt: str
