from typing import Any, Dict, Optional

from .config import settings


def estimate_cost(model: str, usage: Optional[Dict[str, Any]]) -> Optional[float]:
    if not usage:
        return None
    total_tokens = usage.get("total_tokens") or usage.get("total") or 0
    rate = settings.pricing.get(model)
    if rate is None:
        return None
    return round((total_tokens / 1000) * rate, 4)
