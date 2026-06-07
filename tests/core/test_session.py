from rpi_flashcards.core.models import DeckCard, StudyDeck
from rpi_flashcards.core.progress import ReviewRating
from rpi_flashcards.core.session import FlashcardSession


def build_test_deck() -> StudyDeck:
    return StudyDeck(
        deck_id="test-deck",
        title="Test Deck",
        description="Deck for session tests.",
        cards=(
            DeckCard(
                card_id="card-1",
                entry_id="entry-1",
                lemma="adapt",
                part_of_speech="verb",
                definition="to change to fit a new situation",
            ),
            DeckCard(
                card_id="card-2",
                entry_id="entry-2",
                lemma="careful",
                part_of_speech="adjective",
                definition="taking time to avoid mistakes",
            ),
        ),
    )


def test_reveal_and_next_reset_visibility() -> None:
    session = FlashcardSession(build_test_deck())

    assert session.current_card.lemma == "adapt"
    assert session.is_revealed is False

    session.reveal_current()
    assert session.is_revealed is True

    session.next_card()
    assert session.current_card.lemma == "careful"
    assert session.is_revealed is False


def test_rating_appends_review_event() -> None:
    session = FlashcardSession(build_test_deck(), clock=lambda: "2026-04-06T00:00:00+00:00")

    event = session.rate_current(ReviewRating.GOOD)

    assert event.rating == "good"
    assert session.history.events[-1].lemma == "adapt"
    assert session.history.events[-1].occurred_at == "2026-04-06T00:00:00+00:00"

