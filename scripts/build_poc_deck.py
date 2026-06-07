from __future__ import annotations

from pathlib import Path

from rpi_flashcards.data.deck_builder import DeckBuildConfig, build_deck, save_deck
from rpi_flashcards.data.io import read_jsonl


def main() -> None:
    config = DeckBuildConfig.from_toml(Path("configs/decks/poc.toml"))
    deck = build_deck(read_jsonl(Path("data/normalized/seed_entries.jsonl")), config)
    save_deck(deck, Path("data/decks/poc_deck.json"))


if __name__ == "__main__":
    main()

