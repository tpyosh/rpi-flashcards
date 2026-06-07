import pytest

from rpi_flashcards.data.normalize import normalize_seed_entry, validate_normalized_entry


def test_normalize_seed_entry_shapes_fields() -> None:
    normalized = normalize_seed_entry(
        {
            "source_id": "seed-001",
            "word": "Adapt",
            "pos": "Verb",
            "gloss": "to change to fit a new purpose or situation",
            "example": "Plants adapt to dry climates over time.",
            "difficulty": "A2",
            "frequency_per_million": 7.8,
            "tags": ["poc", "change"],
        }
    )

    assert normalized["lemma"] == "adapt"
    assert normalized["part_of_speech"] == "verb"
    assert normalized["source"] == "manual_seed"


def test_validate_normalized_entry_rejects_missing_definition() -> None:
    with pytest.raises(ValueError):
        validate_normalized_entry(
            {
                "entry_id": "seed-001",
                "lemma": "adapt",
                "part_of_speech": "verb",
                "definition": "",
                "tags": ["poc"],
                "source": "manual_seed",
            }
        )

