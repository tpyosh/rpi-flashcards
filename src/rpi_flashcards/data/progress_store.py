from __future__ import annotations

from pathlib import Path

from rpi_flashcards.core.progress import ReviewHistory
from rpi_flashcards.data.io import read_json, write_json


def load_review_history(path: Path, deck_id: str) -> ReviewHistory:
    if not path.exists():
        return ReviewHistory(deck_id=deck_id)
    return ReviewHistory.from_record(read_json(path))


def save_review_history(history: ReviewHistory, path: Path) -> None:
    write_json(path, history.to_record())

