import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import settings
from .pipeline import create_run, run_pipeline
from .storage import list_items, save

TOPIC_SLOTS = ["work1", "work2", "edu1", "edu2", "luck1"]

data_dir = settings.data_dir
job_queue: asyncio.Queue[str] = asyncio.Queue()


def _latest_topic_file() -> Optional[Path]:
    topic_dir = data_dir / "topics"
    files = sorted(topic_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _placeholder_topics() -> List[Dict[str, Any]]:
    return [
        {
            "slot": "work1",
            "category": "work",
            "title": "Stability of energy storage supply chains",
            "why_it_matters": "Impacts project on grid-edge infra.",
            "launch_prompt": "Assess near-term supply risks for Li-ion storage integrators across US/EU/China.",
            "suggested_depth": "normal",
            "falsifiers": ["Integration margins remain stable and lead times shrink within 12 months."],
        },
        {
            "slot": "work2",
            "category": "work",
            "title": "Broker routing modernization",
            "why_it_matters": "Supports market-structure project.",
            "launch_prompt": "Which brokers are leading adoption of order-by-order routing optimizations in US equities?",
            "suggested_depth": "quick",
            "falsifiers": ["No measurable execution improvement vs VWAP in pilot venues."],
        },
        {
            "slot": "edu1",
            "category": "education",
            "title": "Options gamma scalping primer",
            "why_it_matters": "Skill growth for PM around intraday hedging.",
            "launch_prompt": "Teach me gamma scalping playbooks with concrete PnL sensitivities and risk controls.",
            "suggested_depth": "normal",
            "falsifiers": ["PnL examples ignore transaction costs."],
        },
        {
            "slot": "edu2",
            "category": "education",
            "title": "Clearinghouse risk waterfalls",
            "why_it_matters": "Improve understanding of CCP default management.",
            "launch_prompt": "Explain CCP risk waterfalls with historic stress scenarios and where equity is at risk.",
            "suggested_depth": "normal",
            "falsifiers": ["No differences across major CCPs are identified."],
        },
        {
            "slot": "luck1",
            "category": "serendipity",
            "title": "10-year fiber bottlenecks",
            "why_it_matters": "Could shape latency-sensitive strategies.",
            "launch_prompt": "Will transoceanic fiber capex slow meaningfully this decade? Map catalysts and indicators.",
            "suggested_depth": "deep",
            "falsifiers": ["Continued double-digit capacity growth without price impact."],
        },
    ]


def _default_batch() -> Dict[str, Any]:
    return {
        "batch_id": f"batch-{int(datetime.utcnow().timestamp())}",
        "created_at": datetime.utcnow().isoformat(),
        "topics": _placeholder_topics(),
    }


def current_topics() -> Dict[str, Any]:
    latest = _latest_topic_file()
    if latest:
        with latest.open("r", encoding="utf-8") as f:
            return json.load(f)
    batch = _default_batch()
    save("topics", batch["batch_id"], batch)
    return batch


def refresh_topics() -> Dict[str, Any]:
    batch = _default_batch()
    save("topics", batch["batch_id"], batch)
    return batch


def replace_slot(slot: str) -> Dict[str, Any]:
    batch = current_topics()
    replacements = [t for t in _placeholder_topics() if t["slot"] == slot]
    if replacements:
        new_topic = replacements[0]
    else:
        new_topic = {
            "slot": slot,
            "category": "work" if slot.startswith("work") else "education" if slot.startswith("edu") else "serendipity",
            "title": "Fresh topic",
            "why_it_matters": "Automatic replacement",
            "launch_prompt": "Generate a new research question for this category.",
            "suggested_depth": "quick",
            "falsifiers": ["Replacement stub"],
        }
    batch["topics"] = [t for t in batch["topics"] if t["slot"] != slot] + [new_topic]
    save("topics", batch["batch_id"], batch)
    return batch


async def worker() -> None:
    while True:
        run_id = await job_queue.get()
        await run_pipeline(run_id)
        job_queue.task_done()


def enqueue_run(run_id: str) -> None:
    job_queue.put_nowait(run_id)


def start_workers() -> None:
    asyncio.create_task(worker())


def schedule_weekly_refresh() -> None:
    async def refresher() -> None:
        while True:
            refresh_topics()
            await asyncio.sleep(timedelta(days=7).total_seconds())

    asyncio.create_task(refresher())
