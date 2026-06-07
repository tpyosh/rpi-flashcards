from __future__ import annotations

import argparse
from pathlib import Path

from rpi_flashcards.data.deck_builder import DeckBuildConfig, build_deck, load_deck, save_deck
from rpi_flashcards.data.io import read_jsonl
from rpi_flashcards.data.normalize import normalize_seed_file
from rpi_flashcards.ui_terminal.app import run_terminal_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rpi-flashcards")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("demo", help="Run the terminal flashcard proof of concept.")
    demo_parser.add_argument("--deck", type=Path, required=True)
    demo_parser.add_argument("--state", type=Path, required=True)

    normalize_parser = subparsers.add_parser(
        "normalize-data", help="Normalize the bundled sample source data into JSONL."
    )
    normalize_parser.add_argument("--source", type=Path, required=True)
    normalize_parser.add_argument("--output", type=Path, required=True)

    build_parser_cmd = subparsers.add_parser(
        "build-deck", help="Build a deterministic deck from normalized entries and a TOML config."
    )
    build_parser_cmd.add_argument("--entries", type=Path, required=True)
    build_parser_cmd.add_argument("--config", type=Path, required=True)
    build_parser_cmd.add_argument("--output", type=Path, required=True)

    preview_parser = subparsers.add_parser(
        "preview-render", help="Render the first card of a deck to a PNG preview."
    )
    preview_parser.add_argument("--deck", type=Path, required=True)
    preview_parser.add_argument("--output", type=Path, required=True)
    preview_parser.add_argument("--revealed", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        run_terminal_demo(deck_path=args.deck, state_path=args.state)
        return

    if args.command == "normalize-data":
        normalize_seed_file(args.source, args.output)
        return

    if args.command == "build-deck":
        entries = [record for record in read_jsonl(args.entries)]
        config = DeckBuildConfig.from_toml(args.config)
        deck = build_deck(entries, config)
        save_deck(deck, args.output)
        return

    if args.command == "preview-render":
        from rpi_flashcards.display.layout import prepare_card_frame
        from rpi_flashcards.display.preview import render_frame_to_png

        deck = load_deck(args.deck)
        frame = prepare_card_frame(
            deck.cards[0],
            revealed=args.revealed,
            card_number=1,
            total_cards=len(deck.cards),
        )
        render_frame_to_png(frame, args.output)
        return

    parser.error("Unsupported command.")


if __name__ == "__main__":
    main()
