from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: str
    name: str
    description: str
    active: bool = True
    created_at: str
    updated_at: Optional[str] = None


class ProjectCreate(BaseModel):
    name: str
    description: str
    active: bool = True
