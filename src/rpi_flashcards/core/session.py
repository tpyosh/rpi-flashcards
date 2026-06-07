from __future__ import annotations

from collections.abc import Callable

from rpi_flashcards.core.models import DeckCard, StudyDeck
from rpi_flashcards.core.progress import ReviewEvent, ReviewHistory, ReviewRating, utc_now_iso


class FlashcardSession:
    def __init__(
        self,
        deck: StudyDeck,
        history: ReviewHistory | None = None,
        clock: Callable[[], str] = utc_now_iso,
    ) -> None:
        if not deck.cards:
            raise ValueError("Study deck must contain at least one card.")
        self.deck = deck
        self.history = history or ReviewHistory(deck_id=deck.deck_id)
        self._clock = clock
        self._index = 0
        self._revealed = False

    @property
    def current_index(self) -> int:
        return self._index

    @property
    def current_card(self) -> DeckCard:
        return self.deck.cards[self._index]

    @property
    def is_revealed(self) -> bool:
        return self._revealed

    def reveal_current(self) -> DeckCard:
        self._revealed = True
        return self.current_card

    def next_card(self) -> DeckCard:
        self._index = (self._index + 1) % len(self.deck.cards)
        self._revealed = False
        return self.current_card

    def rate_current(self, rating: ReviewRating) -> ReviewEvent:
        event = ReviewEvent(
            deck_id=self.deck.deck_id,
            card_id=self.current_card.card_id,
            lemma=self.current_card.lemma,
            rating=rating.value,
            revealed=self._revealed,
            occurred_at=self._clock(),
        )
        self.history.append(event)
        return event
