PYTHON ?= python3
PYTHONPATH := src

.PHONY: setup lint test run-demo normalize-data build-deck preview-render pi-notes

setup:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ruff check src tests scripts

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest

run-demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m rpi_flashcards.cli demo --deck data/decks/poc_deck.json --state state/demo-progress.json

normalize-data:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/normalize_sample.py

build-deck:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/build_poc_deck.py

preview-render:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/preview_first_card.py

pi-notes:
	cat docs/hardware.md

