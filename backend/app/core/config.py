import os
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel


class ModelPricing(BaseModel):
    model: str
    cost_per_1k_tokens: float


class Settings(BaseModel):
    data_dir: Path = Path(__file__).resolve().parent.parent.parent / "data"
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_endpoint: str = os.getenv("OPENROUTER_ENDPOINT", "https://openrouter.ai/api/v1/chat/completions")
    openrouter_referer: str = os.getenv("OPENROUTER_REFERER", "http://localhost:5173")
    openrouter_title: str = os.getenv("OPENROUTER_TITLE", "CouncilLab")
    default_council_models: List[str] = (
        os.getenv(
            "COUNCIL_MODELS",
            "openai/gpt-5.2-pro,anthropic/claude-opus-4.5,google/gemini-3-pro-preview",
        ).split(",")
    )
    chairman_model: str = os.getenv("CHAIRMAN_MODEL", "openai/gpt-5.2-pro")
    pricing: Dict[str, float] = {
        "openai/gpt-5.2-pro": 10.0,
        "anthropic/claude-opus-4.5": 15.0,
        "google/gemini-3-pro-preview": 8.0,
    }

    def ensure_data_dirs(self) -> None:
        for sub in ["runs", "templates", "projects", "topics"]:
            (self.data_dir / sub).mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_data_dirs()
    return settings


settings = get_settings()
