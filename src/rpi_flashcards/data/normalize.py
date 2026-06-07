from __future__ import annotations

from pathlib import Path
from typing import Any

from rpi_flashcards.core.models import DictionaryEntry
from rpi_flashcards.data.io import read_json, write_jsonl

REQUIRED_NORMALIZED_FIELDS = {
    "entry_id",
    "lemma",
    "part_of_speech",
    "definition",
    "tags",
    "source",
}

ALLOWED_PARTS_OF_SPEECH = {"noun", "verb", "adjective", "adverb"}


def validate_normalized_entry(record: dict[str, Any]) -> None:
    missing = REQUIRED_NORMALIZED_FIELDS.difference(record)
    if missing:
        raise ValueError(f"Normalized entry missing fields: {sorted(missing)}")
    if not str(record["lemma"]).strip():
        raise ValueError("Normalized entry lemma must not be empty.")
    if not str(record["definition"]).strip():
        raise ValueError("Normalized entry definition must not be empty.")
    if str(record["part_of_speech"]) not in ALLOWED_PARTS_OF_SPEECH:
        raise ValueError(f"Unsupported part of speech: {record['part_of_speech']}")
    if not isinstance(record["tags"], list):
        raise ValueError("Normalized entry tags must be a list.")
    if (
        record.get("frequency_per_million") is not None
        and float(record["frequency_per_million"]) < 0
    ):
        raise ValueError("Frequency must be non-negative.")


def normalize_seed_entry(record: dict[str, Any]) -> dict[str, Any]:
    normalized = DictionaryEntry(
        entry_id=str(record["source_id"]),
        lemma=str(record["word"]).strip().lower(),
        part_of_speech=str(record["pos"]).strip().lower(),
        definition=str(record["gloss"]).strip(),
        example=(str(record["example"]).strip() if record.get("example") else None),
        difficulty=(str(record["difficulty"]).strip() if record.get("difficulty") else None),
        frequency_per_million=(
            float(record["frequency_per_million"])
            if record.get("frequency_per_million") is not None
            else None
        ),
        tags=tuple(str(tag) for tag in record.get("tags", [])),
        source="manual_seed",
    ).to_record()
    validate_normalized_entry(normalized)
    return normalized


def normalize_seed_file(source_path: Path, output_path: Path) -> list[dict[str, Any]]:
    rows = read_json(source_path)
    normalized_rows = [normalize_seed_entry(row) for row in rows]
    write_jsonl(output_path, normalized_rows)
    return normalized_rows
