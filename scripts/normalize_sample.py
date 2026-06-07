from __future__ import annotations

from pathlib import Path

from rpi_flashcards.data.normalize import normalize_seed_file


def main() -> None:
    normalize_seed_file(
        Path("data/raw/manual_seed/seed_dictionary.json"),
        Path("data/normalized/seed_entries.jsonl"),
    )


if __name__ == "__main__":
    main()

