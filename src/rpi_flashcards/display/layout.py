from __future__ import annotations

import textwrap

from rpi_flashcards.core.models import DeckCard
from rpi_flashcards.display.base import PreparedCardFrame


def _wrap(text: str, width: int) -> tuple[str, ...]:
    return tuple(textwrap.wrap(text, width=width)) or ("",)


def prepare_card_frame(
    card: DeckCard,
    *,
    revealed: bool,
    card_number: int,
    total_cards: int,
    width: int = 250,
    height: int = 122,
) -> PreparedCardFrame:
    title = card.lemma
    subtitle = card.part_of_speech
    if not revealed:
        body_lines = (
            "Definition hidden.",
            "Reveal before sending to the display.",
        )
    else:
        body_lines = ("Definition:", *_wrap(card.definition, width=30))
        if card.example:
            body_lines = (*body_lines, "", "Example:", *_wrap(card.example, width=30))
    footer = f"Card {card_number}/{total_cards} | {card.difficulty or 'n/a'}"
    return PreparedCardFrame(
        width=width,
        height=height,
        title=title,
        subtitle=subtitle,
        body_lines=body_lines,
        footer=footer,
    )

