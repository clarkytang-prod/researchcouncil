import random
import re
from typing import Dict


LETTERS = ["A", "B", "C"]


def assign_letters(models: list[str]) -> Dict[str, str]:
    shuffled = LETTERS.copy()
    random.shuffle(shuffled)
    return {letter: model for letter, model in zip(shuffled, models)}


def scrub_text(text: str) -> str:
    text = re.sub(r"^As .*?,", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"(?i)(gpt|claude|gemini|llama)[^\s]*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
