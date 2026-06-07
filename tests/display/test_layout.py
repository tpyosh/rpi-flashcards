from rpi_flashcards.core.models import DeckCard
from rpi_flashcards.display.layout import prepare_card_frame


def build_card() -> DeckCard:
    return DeckCard(
        card_id="card-1",
        entry_id="entry-1",
        lemma="gather",
        part_of_speech="verb",
        definition="to bring people or things together",
        example="We gather ideas in a shared notebook.",
        difficulty="A2",
    )


def test_hidden_frame_omits_definition_text() -> None:
    frame = prepare_card_frame(build_card(), revealed=False, card_number=1, total_cards=8)

    assert "Definition hidden." in frame.body_lines
    assert all("bring people" not in line for line in frame.body_lines)


def test_revealed_frame_contains_definition_and_example() -> None:
    frame = prepare_card_frame(build_card(), revealed=True, card_number=1, total_cards=8)

    assert "Definition:" in frame.body_lines
    assert any("bring people or things" in line for line in frame.body_lines)
    assert "Example:" in frame.body_lines
