from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class ReviewRating(StrEnum):
    AGAIN = "again"
    HARD = "hard"
    GOOD = "good"
    EASY = "easy"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class ReviewEvent:
    deck_id: str
    card_id: str
    lemma: str
    rating: str
    revealed: bool
    occurred_at: str

    def to_record(self) -> dict[str, Any]:
        return {
            "deck_id": self.deck_id,
            "card_id": self.card_id,
            "lemma": self.lemma,
            "rating": self.rating,
            "revealed": self.revealed,
            "occurred_at": self.occurred_at,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> ReviewEvent:
        return cls(
            deck_id=str(record["deck_id"]),
            card_id=str(record["card_id"]),
            lemma=str(record["lemma"]),
            rating=str(record["rating"]),
            revealed=bool(record["revealed"]),
            occurred_at=str(record["occurred_at"]),
        )


@dataclass
class ReviewHistory:
    deck_id: str
    started_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    events: list[ReviewEvent] = field(default_factory=list)

    def append(self, event: ReviewEvent) -> None:
        self.events.append(event)
        self.updated_at = utc_now_iso()

    def to_record(self) -> dict[str, Any]:
        return {
            "deck_id": self.deck_id,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "events": [event.to_record() for event in self.events],
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> ReviewHistory:
        return cls(
            deck_id=str(record["deck_id"]),
            started_at=str(record.get("started_at", utc_now_iso())),
            updated_at=str(record.get("updated_at", utc_now_iso())),
            events=[ReviewEvent.from_record(event) for event in record.get("events", [])],
        )
