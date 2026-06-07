from pathlib import Path

from rpi_flashcards.data.deck_builder import DeckBuildConfig, build_deck
from rpi_flashcards.data.io import read_jsonl


def test_build_deck_respects_target_count_and_filters() -> None:
    config = DeckBuildConfig.from_toml(Path("configs/decks/poc.toml"))
    deck = build_deck(read_jsonl(Path("data/normalized/seed_entries.jsonl")), config)

    assert deck.deck_id == "poc-core-8"
    assert len(deck.cards) == 8
    assert deck.cards[0].lemma == "careful"
    assert all(
        card.frequency_per_million >= 6.0
        for card in deck.cards
        if card.frequency_per_million
    )
