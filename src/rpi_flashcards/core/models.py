from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DictionaryEntry:
    entry_id: str
    lemma: str
    part_of_speech: str
    definition: str
    example: str | None = None
    difficulty: str | None = None
    frequency_per_million: float | None = None
    tags: tuple[str, ...] = ()
    source: str = "unknown"

    def to_record(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "lemma": self.lemma,
            "part_of_speech": self.part_of_speech,
            "definition": self.definition,
            "example": self.example,
            "difficulty": self.difficulty,
            "frequency_per_million": self.frequency_per_million,
            "tags": list(self.tags),
            "source": self.source,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> DictionaryEntry:
        return cls(
            entry_id=str(record["entry_id"]),
            lemma=str(record["lemma"]),
            part_of_speech=str(record["part_of_speech"]),
            definition=str(record["definition"]),
            example=record.get("example"),
            difficulty=record.get("difficulty"),
            frequency_per_million=(
                float(record["frequency_per_million"])
                if record.get("frequency_per_million") is not None
                else None
            ),
            tags=tuple(record.get("tags", [])),
            source=str(record.get("source", "unknown")),
        )


@dataclass(frozen=True)
class DeckCard:
    card_id: str
    entry_id: str
    lemma: str
    part_of_speech: str
    definition: str
    example: str | None = None
    difficulty: str | None = None
    frequency_per_million: float | None = None
    tags: tuple[str, ...] = ()

    def to_record(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "entry_id": self.entry_id,
            "lemma": self.lemma,
            "part_of_speech": self.part_of_speech,
            "definition": self.definition,
            "example": self.example,
            "difficulty": self.difficulty,
            "frequency_per_million": self.frequency_per_million,
            "tags": list(self.tags),
        }

    @classmethod
    def from_entry(cls, entry: DictionaryEntry, card_index: int) -> DeckCard:
        return cls(
            card_id=f"{entry.entry_id}-card-{card_index}",
            entry_id=entry.entry_id,
            lemma=entry.lemma,
            part_of_speech=entry.part_of_speech,
            definition=entry.definition,
            example=entry.example,
            difficulty=entry.difficulty,
            frequency_per_million=entry.frequency_per_million,
            tags=entry.tags,
        )

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> DeckCard:
        return cls(
            card_id=str(record["card_id"]),
            entry_id=str(record["entry_id"]),
            lemma=str(record["lemma"]),
            part_of_speech=str(record["part_of_speech"]),
            definition=str(record["definition"]),
            example=record.get("example"),
            difficulty=record.get("difficulty"),
            frequency_per_million=(
                float(record["frequency_per_million"])
                if record.get("frequency_per_million") is not None
                else None
            ),
            tags=tuple(record.get("tags", [])),
        )


@dataclass(frozen=True)
class StudyDeck:
    deck_id: str
    title: str
    description: str
    cards: tuple[DeckCard, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        return {
            "deck_id": self.deck_id,
            "title": self.title,
            "description": self.description,
            "cards": [card.to_record() for card in self.cards],
            "metadata": self.metadata,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> StudyDeck:
        return cls(
            deck_id=str(record["deck_id"]),
            title=str(record["title"]),
            description=str(record["description"]),
            cards=tuple(DeckCard.from_record(card) for card in record["cards"]),
            metadata=dict(record.get("metadata", {})),
        )
