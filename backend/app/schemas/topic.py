from typing import List

from pydantic import BaseModel


class Topic(BaseModel):
    slot: str
    category: str
    title: str
    why_it_matters: str
    launch_prompt: str
    suggested_depth: str
    falsifiers: List[str]
