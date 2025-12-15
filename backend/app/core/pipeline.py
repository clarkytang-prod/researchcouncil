import asyncio
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .anonymize import assign_letters, scrub_text
from .config import settings
from .cost import estimate_cost
from .openrouter import run_parallel, safe_chat_completion
from .storage import load, save

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _now() -> str:
    return datetime.utcnow().isoformat()


def _render(template: str, context: Dict[str, Any]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def _load_prompt(name: str) -> Dict[str, Any]:
    with (PROMPTS_DIR / name).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _artifacts_from_stage(run: Dict[str, Any], stage_name: str) -> List[Dict[str, Any]]:
    for stage in run["stages"]:
        if stage["stage_name"] == stage_name:
            return stage["artifacts"]
    return []


def create_run(prompt: str, pipeline: str = "lite", mode: str = "live") -> Dict[str, Any]:
    run_id = f"run-{int(datetime.utcnow().timestamp())}-{random.randint(1000,9999)}"
    base = {
        "run_id": run_id,
        "created_at": _now(),
        "mode": mode,
        "pipeline": pipeline,
        "topic_prompt": prompt,
        "models": settings.default_council_models,
        "chairman_model": settings.chairman_model,
        "status": "queued" if mode == "overnight" else "running",
        "anonymization_map": {},
        "stages": [],
        "final": {},
    }
    save("runs", run_id, base)
    return base


async def run_lite(run_id: str) -> Dict[str, Any]:
    run = load("runs", run_id)
    run["status"] = "running"
    prompts = _load_prompt("council_lite.yaml")

    # Stage 1 Opinions
    s1_template = prompts["stages"]["S1_OPINIONS"]
    s1_requests: List[Dict[str, Any]] = []
    for model in run["models"]:
        messages = [
            {"role": "system", "content": s1_template["system"]},
            {
                "role": "user",
                "content": _render(
                    s1_template["user"],
                    {"PROMPT": run["topic_prompt"], "CONTEXT": "", "SOURCES": ""},
                ),
            },
        ]
        s1_requests.append({"model": model, "messages": messages})

    s1_results = await run_parallel(s1_requests)
    s1_artifacts = []
    for model, resp in zip(run["models"], s1_results):
        message = resp.get("choices", [{}])[0].get("message", {})
        text = message.get("content", "")
        parsed = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        artifact = {
            "model": model,
            "prompt": s1_template["user"],
            "response_text": text,
            "response_json": parsed,
            "usage": resp.get("usage"),
            "cost_estimate_usd": estimate_cost(model, resp.get("usage")),
            "latency_ms": None,
            "error": parsed.get("error") if isinstance(parsed, dict) and "error" in parsed else None,
        }
        s1_artifacts.append(artifact)
    run["stages"].append({"stage_name": "S1_OPINIONS", "status": "completed", "artifacts": s1_artifacts})

    # Stage 2 Review
    s2_template = prompts["stages"]["S2_REVIEW"]
    mapping = assign_letters(run["models"])
    run["anonymization_map"] = mapping
    answers = {}
    for letter, model in mapping.items():
        artifact = next(a for a in s1_artifacts if a["model"] == model)
        answers[letter] = scrub_text(artifact.get("response_text", ""))

    s2_requests: List[Dict[str, Any]] = []
    for model in run["models"]:
        messages = [
            {"role": "system", "content": s2_template["system"]},
            {
                "role": "user",
                "content": _render(
                    s2_template["user"],
                    {
                        "PROMPT": run["topic_prompt"],
                        "ANSWER_A": answers.get("A", ""),
                        "ANSWER_B": answers.get("B", ""),
                        "ANSWER_C": answers.get("C", ""),
                    },
                ),
            },
        ]
        s2_requests.append({"model": model, "messages": messages})

    s2_results = await run_parallel(s2_requests)
    s2_artifacts = []
    for model, resp in zip(run["models"], s2_results):
        message = resp.get("choices", [{}])[0].get("message", {})
        text = message.get("content", "")
        parsed = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        s2_artifacts.append(
            {
                "model": model,
                "prompt": s2_template["user"],
                "response_text": text,
                "response_json": parsed,
                "usage": resp.get("usage"),
                "cost_estimate_usd": estimate_cost(model, resp.get("usage")),
                "latency_ms": None,
                "error": parsed.get("error") if isinstance(parsed, dict) and "error" in parsed else None,
            }
        )
    run["stages"].append({"stage_name": "S2_REVIEW", "status": "completed", "artifacts": s2_artifacts})

    # Stage 3 Chairman
    s3_template = prompts["stages"]["S3_CHAIRMAN"]
    s1_blob = json.dumps(s1_artifacts, indent=2)
    s2_blob = json.dumps(s2_artifacts, indent=2)
    s3_messages = [
        {"role": "system", "content": s3_template["system"]},
        {
            "role": "user",
            "content": _render(
                s3_template["user"],
                {"PROMPT": run["topic_prompt"], "S1_ALL": s1_blob, "S2_ALL": s2_blob},
            ),
        },
    ]
    s3_resp = await safe_chat_completion(model=run["chairman_model"], messages=s3_messages, max_tokens=1500)
    s3_message = s3_resp.get("choices", [{}])[0].get("message", {})
    s3_text = s3_message.get("content", "")
    s3_json = None
    try:
        s3_json = json.loads(s3_text)
    except json.JSONDecodeError:
        s3_json = None
    s3_artifact = {
        "model": run["chairman_model"],
        "prompt": s3_template["user"],
        "response_text": s3_text,
        "response_json": s3_json,
        "usage": s3_resp.get("usage"),
        "cost_estimate_usd": estimate_cost(run["chairman_model"], s3_resp.get("usage")),
        "latency_ms": None,
        "error": s3_json.get("error") if isinstance(s3_json, dict) and "error" in s3_json else None,
    }
    run["stages"].append({"stage_name": "S3_CHAIRMAN", "status": "completed", "artifacts": [s3_artifact]})
    run["final"] = {
        "final_markdown": (s3_json or {}).get("final_markdown") if isinstance(s3_json, dict) else None,
        "final_json": s3_json,
    }
    run["status"] = "completed"
    save("runs", run_id, run)
    return run


async def run_pipeline(run_id: str) -> Dict[str, Any]:
    run = load("runs", run_id)
    pipeline = run.get("pipeline", "lite")
    if pipeline == "lite":
        return await run_lite(run_id)
    run["status"] = "failed"
    save("runs", run_id, run)
    return run
