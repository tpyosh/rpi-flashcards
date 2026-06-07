from __future__ import annotations

from pathlib import Path

from rpi_flashcards.data.deck_builder import load_deck
from rpi_flashcards.display.layout import prepare_card_frame
from rpi_flashcards.display.preview import render_frame_to_png


def main() -> None:
    deck = load_deck(Path("data/decks/poc_deck.json"))
    frame = prepare_card_frame(
        deck.cards[0],
        revealed=True,
        card_number=1,
        total_cards=len(deck.cards),
    )
    render_frame_to_png(frame, Path("artifacts/preview-first-card.png"))


if __name__ == "__main__":
    main()
