import json
from pathlib import Path
from typing import Any, Dict, List

from .config import settings


def _path(kind: str, identifier: str) -> Path:
    return settings.data_dir / kind / f"{identifier}.json"


def save(kind: str, identifier: str, payload: Dict[str, Any]) -> None:
    path = _path(kind, identifier)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load(kind: str, identifier: str) -> Dict[str, Any]:
    path = _path(kind, identifier)
    if not path.exists():
        raise FileNotFoundError(identifier)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_items(kind: str) -> List[Dict[str, Any]]:
    base = settings.data_dir / kind
    results: List[Dict[str, Any]] = []
    for file in base.glob("*.json"):
        with file.open("r", encoding="utf-8") as f:
            results.append(json.load(f))
    return sorted(results, key=lambda r: r.get("created_at", ""), reverse=True)
