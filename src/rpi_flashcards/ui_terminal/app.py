from __future__ import annotations

from pathlib import Path

from rpi_flashcards.core.progress import ReviewRating
from rpi_flashcards.core.session import FlashcardSession
from rpi_flashcards.data.deck_builder import load_deck
from rpi_flashcards.data.progress_store import (
    load_review_history,
    save_review_history,
)

COMMAND_HELP = "Commands: [r]eveal [n]ext [1]again [2]hard [3]good [4]easy [q]uit"


def _print_card(session: FlashcardSession) -> None:
    card = session.current_card
    print()
    print(f"Card {session.current_index + 1}/{len(session.deck.cards)}")
    print(f"{card.lemma} ({card.part_of_speech})")
    if session.is_revealed:
        print(f"Definition: {card.definition}")
        if card.example:
            print(f"Example: {card.example}")
        print(f"Difficulty bucket: {card.difficulty or 'n/a'}")
    else:
        print("Definition: [hidden]")
    print(COMMAND_HELP)


def run_terminal_demo(deck_path: Path, state_path: Path) -> None:
    deck = load_deck(deck_path)
    history = load_review_history(state_path, deck.deck_id)
    session = FlashcardSession(deck=deck, history=history)

    print(f"Loaded deck: {deck.title}")
    print(deck.description)

    while True:
        _print_card(session)
        command = input("> ").strip().lower()
        if command == "q":
            save_review_history(session.history, state_path)
            print("Progress saved. Bye.")
            return
        if command == "r":
            session.reveal_current()
            continue
        if command == "n":
            session.next_card()
            continue
        if command in {"1", "2", "3", "4"}:
            rating = {
                "1": ReviewRating.AGAIN,
                "2": ReviewRating.HARD,
                "3": ReviewRating.GOOD,
                "4": ReviewRating.EASY,
            }[command]
            session.rate_current(rating)
            save_review_history(session.history, state_path)
            session.next_card()
            continue
        print("Unknown command.")
