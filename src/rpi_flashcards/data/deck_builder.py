from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rpi_flashcards.core.models import DeckCard, DictionaryEntry, StudyDeck
from rpi_flashcards.data.io import read_json, write_json
from rpi_flashcards.data.normalize import validate_normalized_entry


@dataclass(frozen=True)
class DeckBuildConfig:
    deck_id: str
    title: str
    description: str
    target_count: int
    allowed_parts_of_speech: tuple[str, ...]
    difficulty_buckets: tuple[str, ...] = ()
    min_frequency_per_million: float | None = None
    max_frequency_per_million: float | None = None
    required_tags: tuple[str, ...] = ()
    include_examples: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_toml(cls, path: Path) -> DeckBuildConfig:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
        selection = payload["selection"]
        return cls(
            deck_id=str(payload["deck_id"]),
            title=str(payload["title"]),
            description=str(payload["description"]),
            target_count=int(selection["target_count"]),
            allowed_parts_of_speech=tuple(selection.get("allowed_parts_of_speech", [])),
            difficulty_buckets=tuple(selection.get("difficulty_buckets", [])),
            min_frequency_per_million=selection.get("min_frequency_per_million"),
            max_frequency_per_million=selection.get("max_frequency_per_million"),
            required_tags=tuple(selection.get("required_tags", [])),
            include_examples=bool(selection.get("include_examples", True)),
            metadata={"selection": selection},
        )


def _matches_filters(entry: DictionaryEntry, config: DeckBuildConfig) -> bool:
    if (
        config.allowed_parts_of_speech
        and entry.part_of_speech not in config.allowed_parts_of_speech
    ):
        return False
    if config.difficulty_buckets and entry.difficulty not in config.difficulty_buckets:
        return False
    if config.required_tags and not set(config.required_tags).issubset(set(entry.tags)):
        return False
    if (
        config.min_frequency_per_million is not None
        and entry.frequency_per_million is not None
        and entry.frequency_per_million < config.min_frequency_per_million
    ):
        return False
    if (
        config.max_frequency_per_million is not None
        and entry.frequency_per_million is not None
        and entry.frequency_per_million > config.max_frequency_per_million
    ):
        return False
    return True


def select_entries(records: list[dict[str, Any]], config: DeckBuildConfig) -> list[DictionaryEntry]:
    entries: list[DictionaryEntry] = []
    for record in records:
        validate_normalized_entry(record)
        entry = DictionaryEntry.from_record(record)
        if _matches_filters(entry, config):
            entries.append(entry)
    entries.sort(key=lambda entry: (-(entry.frequency_per_million or 0.0), entry.lemma))
    return entries[: config.target_count]


def build_deck(records: list[dict[str, Any]], config: DeckBuildConfig) -> StudyDeck:
    selected_entries = select_entries(records, config)
    cards = []
    for index, entry in enumerate(selected_entries, start=1):
        card = DeckCard.from_entry(entry, index)
        if not config.include_examples:
            card = DeckCard(
                card_id=card.card_id,
                entry_id=card.entry_id,
                lemma=card.lemma,
                part_of_speech=card.part_of_speech,
                definition=card.definition,
                difficulty=card.difficulty,
                frequency_per_million=card.frequency_per_million,
                tags=card.tags,
            )
        cards.append(card)
    return StudyDeck(
        deck_id=config.deck_id,
        title=config.title,
        description=config.description,
        cards=tuple(cards),
        metadata=config.metadata,
    )


def save_deck(deck: StudyDeck, output_path: Path) -> None:
    write_json(output_path, deck.to_record())


def load_deck(path: Path) -> StudyDeck:
    return StudyDeck.from_record(read_json(path))
